import pytest
from WeatherFetcher import WeatherFetcher
from WeatherProcessor import WeatherProcessor

def test_WeatherFetcher():
    lat = 51.5074
    long = 0.1278
    weather = WeatherFetcher(lat, long)
    assert "hourly" in weather
    assert "time" in weather["hourly"]
    assert "temperature_2m" in weather["hourly"]
    assert "rain" in weather["hourly"]

def test_WeatherProcessor():
    city = "Wrocław"
    time = [1, 2, 3]
    temp = [5, 10, 15]
    rain = [0.2, 0.4, 0.6]
    x = 6
    y = 0.5
    expected_output = f"Warning {city}, Low temperature 5 of C and rain 0.2 mm expected on 1\n"
    expected_output += f"Warning {city}, Low temperature 15 of C and rain 0.6 mm expected on 3\n"
    # captured_output = pytest.capture_stdout()
    # with captured_output:
    #     WeatherProcessor(city, time, temp, rain, x, y)
    # assert captured_output.getvalue() == expected_output