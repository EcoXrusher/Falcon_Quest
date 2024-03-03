import argparse
import requests
import asyncio

latitude = 51.5074
longitude  = 0.1278
city = "Wrocław"
async def WeatherFetcher(lat,long,it):
    print(f"Fetching weather data iter {it}")
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        # "q": "Wrocław",
        "latitude": lat,
        "longitude": long,
        "hourly": {"temperature_2m", "rain"}
        }
    await asyncio.sleep(0.1)
    response = requests.get(url, params=params).json()
    data = {}
    data["time"] = response["hourly"]["time"]
    data["temperature_2m"] = response["hourly"]["temperature_2m"]
    data["rain"] = response["hourly"]["rain"]
    return data



async def WeatherProcessor(city, time, temp, rain , x, y, it):
    for time, temp, rain in zip(time, temp, rain):
        if(temp < x or rain > y):
            print(f"Warning {city}, Low temperature {temp} of C and rain {rain} mm expected on {time}, iter {it}")
        


async def AsyncioEventLoop(x,y,n):
    data = await WeatherFetcher(latitude,longitude,n)
    await WeatherProcessor(city, data["time"], data["temperature_2m"], data["rain"], x, y,n)

async def main(t,r):
    await asyncio.gather(*(AsyncioEventLoop(t,r,n) for  n in range(10)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weather Fetcher")
    parser.add_argument("-t", type=float, help="Temperature threshold")
    parser.add_argument("-r", type=float, help="Rain threshold")
    args = parser.parse_args()
    import time
    s = time.perf_counter()
    asyncio.run(main(args.t,args.r))
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")