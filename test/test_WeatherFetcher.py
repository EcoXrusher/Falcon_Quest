# import pytest
# from WFP.WeatherFetcher import weather_fetcher
# from unittest.mock import AsyncMock, patch, Mock

# @pytest.mark.asyncio
# @patch('WFP.WeatherFetcher.geo_locator.geocode', new_callable=Mock)
# async def test_weather_fetcher_success():
#   await weather_fetcher('Gdynia')