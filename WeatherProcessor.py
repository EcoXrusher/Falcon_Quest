async def WeatherProcessor(city, time, temp, rain , x, y, it) -> None:
    for time, temp, rain in zip(time, temp, rain):
        if(temp < x or rain > y):
            print(f"Warning {city}, Low temperature {temp} of C and rain {rain} mm expected on {time}, iter {it}")