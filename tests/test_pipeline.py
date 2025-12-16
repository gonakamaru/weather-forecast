from unittest.mock import MagicMock
from src.orchestration.pipeline import WeatherPipeline


def test_run_happy_path(mocker):
    pipeline = WeatherPipeline()

    # Arrange
    fake_chart = MagicMock()
    fake_images = MagicMock()
    fake_forecast = MagicMock()

    mock_download = mocker.patch.object(
        pipeline, "_download_chart", return_value=fake_chart
    )
    mock_should = mocker.patch.object(pipeline, "_should_process", return_value=True)

    mock_prepare = mocker.patch.object(
        pipeline, "_prepare_images", return_value=fake_images
    )
    mock_generate = mocker.patch.object(
        pipeline, "_generate_forecast", return_value=fake_forecast
    )
    mock_publish = mocker.patch.object(pipeline, "_publish")

    # Act
    pipeline.run()

    # Assert
    mock_download.assert_called_once_with()
    mock_should.assert_called_once_with(fake_chart)
    mock_prepare.assert_called_once_with(fake_chart)
    mock_generate.assert_called_once_with(fake_images)
    mock_publish.assert_called_once_with(fake_images, fake_forecast)


def test_run_skips_when_should_process_is_false(mocker):
    pipeline = WeatherPipeline()

    # Arrange
    fake_chart = MagicMock()

    mock_download = mocker.patch.object(
        pipeline, "_download_chart", return_value=fake_chart
    )
    mock_should = mocker.patch.object(pipeline, "_should_process", return_value=False)

    mock_prepare = mocker.patch.object(pipeline, "_prepare_images")
    mock_generate = mocker.patch.object(pipeline, "_generate_forecast")
    mock_publish = mocker.patch.object(pipeline, "_publish")

    # Act
    pipeline.run()

    # Assert
    mock_download.assert_called_once_with()
    mock_should.assert_called_once_with(fake_chart)
    mock_prepare.assert_not_called()
    mock_generate.assert_not_called()
    mock_publish.assert_not_called()
