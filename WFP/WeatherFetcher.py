# import asyncio
import aiohttp
import requests
import os

async def WeatherFetcher(city) -> dict:
    API_KEY = os.getenv("API_KEY")
    print(f"Fetching weather data for {city}...")
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    geo_params = {
        "q": city,
        "limit": 1,
        'appid': API_KEY
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(geo_url, params=geo_params) as response:
                if response.status != 200:
                    raise Exception (f"HTTP{response.status}")
                geo_res = await response.json()
    except Exception as e:
        print(f"Error fetching city data for {city}: {e}")
        return {}
    latitude = geo_res[0]["lat"]
    longitude = geo_res[0]["lon"]
    # print (geo_res)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "rain"]
        }
    # response = requests.get(url, params=params).json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    raise Exception (f"HTTP{response.status}")
                response = await response.json()
    except Exception as e:
        print(f"Error fetching weather data for {city}: {e}")
        return {}
    data = {}
    data["time"] = response["hourly"]["time"]
    data["temperature_2m"] = response["hourly"]["temperature_2m"]
    data["rain"] = response["hourly"]["rain"]
    return data