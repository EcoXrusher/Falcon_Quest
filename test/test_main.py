import pytest
from unittest.mock import AsyncMock, patch, Mock
from WFP.__main__ import caller
from WFP.__main__ import add_task
from WFP.__main__ import main


@pytest.mark.asyncio
@patch('WFP.__main__.weather_fetcher', new_callable=AsyncMock)
@patch('WFP.__main__.weather_processor', new_callable=AsyncMock)
@patch('WFP.__main__.asyncio.sleep', new_callable=AsyncMock)
async def test_caller(mock_sleep, mock_processor, mock_fetcher):
    """
    Test caller function with successful response
    Mocking weather_fetcher and weather_processor.
    Test passes if the function calls weather_fetcher and weather_processor with correct arguments.
    """
    city = 'London'
    expected_time = "12:00"
    expected_temp = 20
    expected_rain = 0
    sleep_time = 5
    temp_treshold = 15
    rain_treshold = 10
    mock_fetcher.return_value = {"time": expected_time, "temperature_2m": expected_temp, "rain": expected_rain}
    run_once = Mock(side_effect=[True, False])
    await caller(city, temp_treshold, rain_treshold, sleep_time, loop_condition=run_once)
    mock_fetcher.assert_called_once_with(city)
    mock_processor.assert_called_once_with(city, expected_time, expected_temp, expected_rain, temp_treshold, rain_treshold)
    mock_sleep.assert_called_once_with(sleep_time)


@pytest.mark.asyncio
@patch('WFP.__main__.weather_fetcher', new_callable=AsyncMock)
async def test_caller_with_empty_data(mock_fetcher, capsys):
    """
    Test caller function with failed response
    Mocking weather_fetcher to return empty dictionary.
    Test passes if the function prints an error message.
    """
    city = 'London'
    time = 15
    temp = 10
    rain = 5
    mock_fetcher.return_value = {}
    run_once = Mock(side_effect=[True, False])
    await caller(city,time,temp,rain,loop_condition=run_once)
    mock_fetcher.assert_called_once_with('London')
    captured = capsys.readouterr()
    assert "Error fetching weather data for London" in captured.out


@patch('WFP.__main__.asyncio.create_task', new_callable=Mock)
@patch('WFP.__main__.caller', new_callable=Mock)
def test_add_task(mock_caller, mock_create_task):
    """
    Test add_task function
    Mocking caller and create_task.
    Test passes if the function calls create_task with correct arguments.
    """
    city = 'London'
    time = 15
    temp = 10
    rain = 5
    add_task(city, temp, rain, time)
    mock_create_task.assert_called_once_with(mock_caller(city, temp, rain, time))