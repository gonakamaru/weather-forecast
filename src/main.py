# Weather Forecast + Salesforce
#
# License:
#   MIT License
#
# Enjoy coding! 🛸
# ==========================================
from pathlib import Path
from src.cli.app import parse_args
from src.salesforce.weather import SFWeatherClient
from src.orchestration.pipeline import WeatherPipeline

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

    pipeline = WeatherPipeline()

    chart = pipeline._download_chart()
    updated, pdf_hash, pdf_path = chart["updated"], chart["hash"], chart["path"]

    if pipeline._should_process(chart):

        images = pipeline._prepare_images(chart)

        # print("salesforce")
        # sf = SFWeatherClient()
        # records = sf.find_or_create_report(pdf_hash)
        # print(records)
        # record_id = records[0]["Id"]
        # print(record_id)

        # cv_id = sf.ensure_preview_image(record_id, images["small"])

        # if cv_id:
        #     print("Uploaded new ContentVersion:", cv_id)
        # else:
        #     print("small.png already exists, skipping.")

        forecast = pipeline._generate_forecast(images)

        # sf.update_forecast(record_id, forecast["content"])
        # print("Updated forecast in Salesforce.")

        pipeline._publish_salesforce(chart, images, forecast)


if __name__ == "__main__":
    main()
