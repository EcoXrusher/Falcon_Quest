# tests/__main__.py

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
    mock_fetcher.return_value = {"time": "12:00", "temperature_2m": 20, "rain": 0}
    run_once = Mock(side_effect=[True, False])
    await caller('London', 15, 10, 5,loop_condition=run_once)
    mock_fetcher.assert_called_once_with('London')
    mock_processor.assert_called_once_with('London', "12:00", 20, 0, 15, 10)
    mock_sleep.assert_called_once_with(5)


@pytest.mark.asyncio
@patch('WFP.__main__.weather_fetcher', new_callable=AsyncMock)
async def test_caller_with_empty_data(mock_fetcher, capsys):
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
    city = 'London'
    time = 15
    temp = 10
    rain = 5
    add_task(city, temp, rain, time)
    mock_create_task.assert_called_once_with(mock_caller(city, temp, rain, time))

# import asyncio.tasks.Task.cancel
import argparse
@pytest.mark.asyncio
@patch('WFP.__main__.add_task', new_callable=Mock)
@patch('WFP.__main__.asyncio.Task', new_callable=AsyncMock)
@patch('WFP.__main__.argparse.ArgumentParser.parse_args', new_callable=Mock)
@patch('WFP.__main__.input', new_callable=Mock)
@patch('WFP.__main__.asyncio.gather', new_callable=AsyncMock)
async def test_main(mock_gather, mock_input, mock_parse_args,mock_cancel, mock_add_task):
    mock_parse_args.return_value = argparse.Namespace(t=15, r=10)
    mock_input = Mock(side_effect=['Kraków', 10,'e'])
    await main()
    mock_add_task.assert_called_once_with('Kraków', 15, 10, 10)
    mock_cancel.assert_called_once()
    mock_gather.assert_called_once()
