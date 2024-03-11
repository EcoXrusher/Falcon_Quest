import pytest
from WFP.WeatherFetcher import weather_fetcher


@pytest.mark.asyncio
# @patch('WFP.WeatherFetcher.geo_locator.geocode', new_callable=Mock)
async def test_weather_fetcher_success():
  """
  Test weather_fetcher function with successful response
  Working only with valid city name and internet connetion.

  AIOHTTP is not mocked, so it requires internet connection and valid args.

  Test passes if the function returns a dictionary with weather data.
  """
  data_check = await weather_fetcher('Gdynia')
  assert data_check != {}
  assert "time" in data_check
  assert "temperature_2m" in data_check
  assert "rain" in data_check


@pytest.mark.asyncio
async def test_weather_fetcher_failure():
  """
  Test weather_fetcher function with failed response
  Working only with invalid city name and internet connetion.

  AIOHTTP is not mocked, so it requires internet connection and not existing place.

  Test passes if the function returns an empty dictionary.
  """
  assert {} == await weather_fetcher('NonExistingCity')