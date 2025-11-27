# Weather Forecast + Salesforce
#
# License:
#   MIT License
#
# Enjoy coding! 🛸
# ==========================================
from cli import parse_args
from downloader import WeatherPDFDownloader

WEATHER_PDF_URL = "https://www.data.jma.go.jp/yoho/data/wxchart/quick/ASAS_COLOR.pdf"


def main():
    args = parse_args()

    manager = WeatherPDFDownloader(
        data_dir="./data", weather_pdf_url="https://weather.example.com/latest.pdf"
    )

    result = manager.update()
    print(result)

    manager = WeatherPDFDownloader(
        data_dir="./data",
        weather_pdf_url=WEATHER_PDF_URL,
    )

    result = manager.update()
    print(result)


if __name__ == "__main__":
    main()
