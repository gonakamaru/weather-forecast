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

    if result:
        print("png")
        downloader.create_png()
        small_png_path = downloader.create_small_png(width=300)

        print("salesforce")
        sf = SalesforceClient()
        records = sf.find_or_create_records(pdf_hash)
        print(records)
        record_id = records[0]["Id"]
        print(record_id)

        cv_id = sf.ensure_small_png(record_id, small_png_path)

        if cv_id:
            print("Uploaded new ContentVersion:", cv_id)
        else:
            print("small.png already exists, skipping.")


if __name__ == "__main__":
    main()
