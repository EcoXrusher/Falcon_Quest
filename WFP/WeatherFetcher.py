import aiohttp
from geopy.geocoders import Nominatim

async def weather_fetcher(city) -> dict:
    latitude = None
    longitude = None
    return_data = dict()
    # Fetching cordinates for the city
    geo_locator = Nominatim(user_agent="geoapiTaskTrial")
    location = geo_locator.geocode(city)
    if location:
        print(f'Cordinates for {city} are: {location.latitude}, {location.longitude}')
        latitude = location.latitude
        longitude = location.longitude
    else:
        print(f'No cordinates found for {city}')
        return return_data
    # Fetching weather data for the city
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "rain"]
        }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    raise Exception (f"HTTP{response.status}")
                response = await response.json()
    except Exception as e:
        print(f"Error fetching weather data for {city}: {e}")
        return return_data
    # Extracting data from the response
    return_data["time"] = response["hourly"]["time"]
    return_data["temperature_2m"] = response["hourly"]["temperature_2m"]
    return_data["rain"] = response["hourly"]["rain"]
    return return_data