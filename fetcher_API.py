import requests

latitude = 51.5074
longitude  = 0.1278
def WeatherFetcher(lat,long):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        # "city": "Wrocław",
        "latitude": lat,
        "longitude": long,
        "hourly": {"temperature_2m", "rain"}
        }
    response = requests.get(url, params=params)
    print(response.json())
    file = open("weather.json", "w")
    file.write(response.text)
    file.close()
    return response.json()

if __name__ == "__main__":
    weather = WeatherFetcher(latitude,longitude)
    time = weather["hourly"]["time"]
    temp = weather["hourly"]["temperature_2m"]
    rain = weather["hourly"]["rain"]