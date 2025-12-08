# Weather Forecast + Salesforce
#
# License:
#   MIT License
#
# Enjoy coding! 🛸
# ==========================================
from src.cli import parse_args
from src.downloader import WeatherPDFDownloader

WEATHER_PDF_URL = "https://www.data.jma.go.jp/yoho/data/wxchart/quick/ASAS_COLOR.pdf"


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

    downloader = WeatherPDFDownloader(
        data_dir="./data",
        weather_pdf_url=WEATHER_PDF_URL,
    )

    result, pdf_hash = downloader.update()
    print(f"downloader: {result}, {pdf_hash}")


if __name__ == "__main__":
    main()
