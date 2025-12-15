def test_weather_pipeline_exists():
    from src.orchestration.pipeline import WeatherPipeline

    assert WeatherPipeline is not None
