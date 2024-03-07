import argparse
from WFP.WeatherFetcher import WeatherFetcher
from WFP.WeatherProcessor import WeatherProcessor

import asyncio
tasks = []

async def caller(city,x,y,breakTime) -> None:
    while True:
        data = await WeatherFetcher(city)
        if data == {}:
            print(f"Error fetching weather data for {city}")
            return
        await WeatherProcessor(city, data["time"], data["temperature_2m"], data["rain"], x, y)
        await asyncio.sleep(int(breakTime))


def add_task(city,temp,rain,breakTime):
    tasks.append(asyncio.create_task(caller(city,temp,rain,breakTime)))


async def main():
    parser = argparse.ArgumentParser(description="Weather Fetcher")
    parser.add_argument("-t", type=float, help="Temperature threshold")
    parser.add_argument("-r", type=float, help="Rain threshold")
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    while True:
        UserInput_city = await loop.run_in_executor(None, input, "Enter city: ")
        if UserInput_city == "e":
            break
        UserInput_breakTime = await loop.run_in_executor(None, input, "Enter break time: ")
        add_task(UserInput_city,args.t,args.r,UserInput_breakTime)
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__== "__main__":
    parser = argparse.ArgumentParser(description="Weather Fetcher")
    parser.add_argument("-t", type=float, help="Temperature threshold")
    parser.add_argument("-r", type=float, help="Rain threshold")
    args = parser.parse_args()
    asyncio.run(main())