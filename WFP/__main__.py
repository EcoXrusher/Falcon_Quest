from WFP.WeatherFetcher import weather_fetcher
from WFP.WeatherProcessor import weather_processor


import argparse
import asyncio


# List to store the tasks
tasks = []


async def caller(city : str, x :int , y: float, breakTime : int , loop_condition=lambda: True) -> None:
    """Caller function to fetch and process the weather data for the city provided in async loop.

    Parameters:
    city: str               - city name
    x: int                  - temperature threshold
    y: float                - rain threshold
    breakTime: int          - time interval for fetching the weather data
    loop_condition: function- function to check the condition for the loop

    Returns:
    None
    """
    # Loop to keep fetching the weather data in user input intervals
    while loop_condition():
        # Calling Weather Fetcher
        data = await weather_fetcher(city)
        # Validating output
        if data == {}:
            print(f"Error fetching weather data for {city}")
            return
        # Calling Weather Processor
        await weather_processor(city, data["time"], data["temperature_2m"], data["rain"], x, y)
        # Calling sleep with read interval time
        await asyncio.sleep(int(breakTime))


def add_task(city : str, temp : int, rain : float, breakTime : int) -> None:
    """Add the task to the list of tasks.

    Parameters:
    city: str               - city name
    temp: int               - temperature threshold
    rain: float             - rain threshold
    breakTime: int          - time interval for fetching the weather data

    Returns:
    None
    """
    # Adding the task to the list of tasks
    tasks.append(asyncio.create_task(caller(city,temp,rain,breakTime)))


async def main():
    """Main function to take input from the console, and input form user in the loop.
    It is calling next functions to start process of fetch data and process it.
    After providing 'e' as city input it stops tasks and allows tasks to throw excepetion.
    Tasks are running endless loops so it is required to stop them manually and allow to throw exception.
    
    """
    # Parsing the arguments from the command line
    parser = argparse.ArgumentParser(description="Weather Fetcher")
    parser.add_argument("-t", type=float, help="Temperature threshold")
    parser.add_argument("-r", type=float, help="Rain threshold")
    args = parser.parse_args()
    # Taking input from the user inside the event loop
    loop = asyncio.get_event_loop()
    while True:
        UserInput_city = await loop.run_in_executor(None, input, "Enter city: ")
        # Creaing exit condition
        print(UserInput_city)
        if UserInput_city == "e":
            break
        UserInput_breakTime = await loop.run_in_executor(None, input, "Enter break time: ")
        # Call the add_task function
        add_task(UserInput_city,args.t,args.r,UserInput_breakTime)
    # Cancelling all the tasks
    [task.cancel() for task in tasks]
    # Waiting for all the tasks to be cancelled
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__== "__main__":
    # running the main function
    asyncio.run(main())