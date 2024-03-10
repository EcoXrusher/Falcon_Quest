async def weather_processor(city : str, time : list, temp : list , rain : list, temp_treshold : int, rain_treshold : float) -> None:
    """Procesing data from arguments.
      If temperature is lower than x or rain is higher than y, print warning message.
    
    Parameters:
    city: str   - city name
    time: str   - time of the weather forecast
    temp: int   - temperature in Celsius
    rain: int   - rain in mm
    x: int      - temperature threshold
    y: int      - rain threshold

    Returns:
    None
    """
    for time, temp, rain in zip(time, temp, rain):
        if(temp < temp_treshold or rain > rain_treshold):
            print(f"Warning {city}, Low temperature {temp} of C and rain {rain} mm expected on {time}")