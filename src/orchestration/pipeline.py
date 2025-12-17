from pathlib import Path
from src.chart.downloader import WeatherPDFDownloader
from src.chart.processors.image_tools import resize_png
from src.chart.processors.pdf_tools import pdf_to_png

WEATHER_PDF_URL = "https://www.data.jma.go.jp/yoho/data/wxchart/quick/ASAS_COLOR.pdf"
DATA_DIR = "./data"
WEATHER_PNG = "weather.png"
WEATHER_SMALL_PNG = "weather_small.png"


class WeatherPipeline:
    """Orchestrates the weather forecast workflow."""

    def run(self):
        chart = self._download_chart()

        if not self._should_process(chart):
            return

        images = self._prepare_images(chart)
        forecast = self._generate_forecast(images)
        self._publish(images, forecast)

    def _download_chart(self) -> dict:
        """
        Download the weather chart and return its status.

        Returns:
            dict: A dictionary containing 'updated' (bool), 'hash' (str), and 'path' (Path).
        """
        downloader = WeatherPDFDownloader(Path(DATA_DIR), WEATHER_PDF_URL)

        updated, pdf_hash, pdf_path = downloader.refresh_pdf()

        return {
            "updated": updated,
            "hash": pdf_hash,
            "path": pdf_path,
        }

    def _should_process(self, chart: dict) -> bool:
        """
        Decide whether the pipeline should continue processing.

        Args:
            chart (dict): Output from _download_chart()

        Returns:
            bool: True if processing should continue
        """
        if not chart.get("updated", False):
            return False

        # future:
        # if self.force:
        #     return True
        # if self.dryrun:
        #     return False
        # if not within_schedule_window():
        #     return False

        return True

    def _prepare_images(self, chart: dict) -> dict:
        """
        Prepare PNG images from the downloaded PDF for further processing.

        Args:
            chart (dict): Output from _download_chart()
        Returns:
            dict: Paths to prepared images
        """
        # Convert to PNG for AI and Salesforce
        regular_png_path = pdf_to_png(chart["path"], Path(DATA_DIR) / WEATHER_PNG)

        # Create resized 300px PNG for Salesforce (lightweight)
        small_png_path = resize_png(
            regular_png_path, Path(DATA_DIR) / WEATHER_SMALL_PNG, width=300
        )

        images = {
            "regular": regular_png_path,
            "small": small_png_path,
        }
        return images

    def _generate_forecast(self, images):
        pass

    def _publish(self, images, forecast):
        pass
