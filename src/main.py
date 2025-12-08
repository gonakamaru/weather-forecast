# Weather Forecast + Salesforce
#
# License:
#   MIT License
#
# Enjoy coding! 🛸
# ==========================================
from src.cli import parse_args
from src.downloader import WeatherPDFDownloader
from src.salesforce_client import SalesforceClient

DATA_DIR = "./data"
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
        data_dir=DATA_DIR,
        weather_pdf_url=WEATHER_PDF_URL,
    )

    result, pdf_hash = downloader.update()
    print(f"downloader: {result}, {pdf_hash}")

    if result or True:
        print("salesforce")
        sf = SalesforceClient()

        records = sf.find_or_create_records(pdf_hash)
        print(records)
        if not records:
            print("Records not found")
        else:
            print("Records exists")


if __name__ == "__main__":
    main()
