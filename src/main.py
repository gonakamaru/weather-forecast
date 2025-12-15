# Weather Forecast + Salesforce
#
# License:
#   MIT License
#
# Enjoy coding! 🛸
# ==========================================
from pathlib import Path
from src.cli.app import parse_args
from src.chart.downloader import WeatherPDFDownloader
from src.chart.processors.pdf_tools import pdf_to_png
from src.chart.processors.image_tools import resize_png
from src.salesforce.weather import SFWeatherClient
from src.forecast_ai import WeatherVision

WEATHER_PDF_URL = "https://www.data.jma.go.jp/yoho/data/wxchart/quick/ASAS_COLOR.pdf"
DATA_DIR = "./data"
WEATHER_PNG = "weather.png"
WEATHER_SMALL_PNG = "weather_small.png"


def main():
    args = parse_args()

    print(f"run: {args.run}")
    print(f"force: {args.force}")
    print(f"dryrun: {args.dryrun}")

    if not args.run:
        raise SystemExit("Error: Missing --run. This flag is required.")

    if args.force:
        # Placeholder for force execution logic
        pass

    if args.dryrun:
        # Placeholder for dryrun logic
        pass

    downloader = WeatherPDFDownloader(Path(DATA_DIR), WEATHER_PDF_URL)

    updated, pdf_hash, pdf_path = downloader.refresh_pdf()

    if updated:
        # Convert to PNG for AI and Salesforce
        output_regular_png_path = Path(DATA_DIR) / WEATHER_PNG
        regular_png_path = pdf_to_png(pdf_path, output_regular_png_path)

        # Create resized 300px PNG for Salesforce (lightweight)
        output_small_png_path = Path(DATA_DIR) / WEATHER_SMALL_PNG
        small_png_path = resize_png(regular_png_path, output_small_png_path, width=300)

        print("salesforce")
        sf = SFWeatherClient()
        records = sf.find_or_create_report(pdf_hash)
        print(records)
        record_id = records[0]["Id"]
        print(record_id)

        cv_id = sf.ensure_preview_image(record_id, small_png_path)

        if cv_id:
            print("Uploaded new ContentVersion:", cv_id)
        else:
            print("small.png already exists, skipping.")

        wv = WeatherVision()
        forecast = wv.generate_forecast(
            regular_png_path, "Title and description\n<image>"
        )
        print(forecast)

        lines = forecast.split("\n", 1)  # Split into at most 2 parts
        title = lines[0]
        content = lines[1] if len(lines) > 1 else ""

        sf.update_forecast(record_id, content)
        print("Updated forecast in Salesforce.")


if __name__ == "__main__":
    main()
