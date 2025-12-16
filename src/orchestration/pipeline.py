class WeatherPipeline:
    """Orchestrates the weather forecast workflow."""

    def run(self):
        chart = self._download_chart()

        if not self._should_process(chart):
            return

        images = self._prepare_images(chart)
        forecast = self._generate_forecast(images)
        self._publish(images, forecast)

    def _download_chart(self):
        pass

    def _should_process(self, chart):
        pass

    def _prepare_images(self, chart):
        pass

    def _generate_forecast(self, images):
        pass

    def _publish(self, images, forecast):
        pass
