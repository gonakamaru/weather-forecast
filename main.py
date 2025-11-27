# Weather Forecast + Salesforce
#
# License:
#   MIT License
#
# Enjoy coding! 🛸
# ==========================================
from cli import parse_args
from downloader import WeatherPDFDownloader


def main():
    args = parse_args()

    manager = WeatherPDFDownloader(
        data_dir="./data", weather_pdf_url="https://weather.example.com/latest.pdf"
    )

    result = manager.update()
    print(result)


if __name__ == "__main__":
    main()
