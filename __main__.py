import argparse
import WeatherFetcher
import WeatherProcessor
from dotenv import load_dotenv

import asyncio
load_dotenv()
city = "Wrocław"

async def AsyncioEventLoop(x,y) -> None:
    for iter in range(10):
        data = await WeatherFetcher.WeatherFetcher(city, iter)
        await WeatherProcessor.WeatherProcessor(city, data["time"], data["temperature_2m"], data["rain"], x, y,iter)


if __name__== "__main__":
    parser = argparse.ArgumentParser(description="Weather Fetcher")
    parser.add_argument("-t", type=float, help="Temperature threshold")
    parser.add_argument("-r", type=float, help="Rain threshold")
    args = parser.parse_args()
    import time
    s = time.perf_counter()
    asyncio.run(AsyncioEventLoop(args.t, args.r))
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.5f} seconds.")