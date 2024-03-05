# import asyncio
# import aiohttp
import requests
import os

async def WeatherFetcher(city, it) -> dict:
    API_KEY = os.getenv("API_KEY")
    print(f"Fetching weather data iter {it}")
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    geo_params = {
        "q": city,
        "limit": 1,
        'appid': API_KEY
    }
    geo_res= requests.get(geo_url, params=geo_params).json()
    # async with aiohttp.ClientSession() as session:
    #    async with session.get(geo_url, params=geo_params) as response:
    #        geo_res = await response.json()
    latitude = geo_res[0]["lat"]
    longitude = geo_res[0]["lon"]
    # print (geo_res)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "rain"]
        }
    response = requests.get(url, params=params).json()
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url, params=params) as response:
    #         response = await response.json()
    data = {}
    data["time"] = response["hourly"]["time"]
    data["temperature_2m"] = response["hourly"]["temperature_2m"]
    data["rain"] = response["hourly"]["rain"]
    return data