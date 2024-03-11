import pytest

from WFP.WeatherProcessor import weather_processor


@pytest.mark.asyncio
async def test_weather_processor_output(capsys):
    city = 'London'
    time = ["12:00", "15:00"]
    temp = [20, 25]
    rain = [0, 10]
    temp_treshold = 22
    rain_treshold = 5
    await weather_processor(city, time, temp, rain, temp_treshold, rain_treshold)
    captured = capsys.readouterr()
    assert "Warning London, Low temperature 20 of C and rain 0 mm expected on 12:00" in captured.out
    assert "Warning London, Low temperature 25 of C and rain 10 mm expected on 15:00" in captured.out


@pytest.mark.asyncio
async def test_weather_processor_no_output(capsys):
    city = 'London'
    time = ["12:00", "15:00"]
    temp = [20, 25]
    rain = [0, 0]
    temp_treshold = 5
    rain_treshold = 5
    await weather_processor(city, time, temp, rain, temp_treshold, rain_treshold)
    captured = capsys.readouterr()
    assert captured.out == ''