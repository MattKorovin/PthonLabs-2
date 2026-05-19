import requests
import json

# OpenWeatherMap
W_API_KEY = "226c0c959cf087672dcdf3c53a4d1190"
W_URL = "https://api.openweathermap.org/data/2.5/weather"
W_CITY = "Dronten"

# GetAmbee
G_API_KEY = "6685763fcbb02ecd19fa9111faeeda650e1be9e29ecd73d51b2e6883f8e99285"
G_URL = "https://api.ambeedata.com/weather/latest/by-lat-lng"
G_LAT = 52.532079
G_LON = 5.727108


print("Лабораторная работа №7\nВыполнил: Коровин Матвей\nВариант 3")
print("Нажмите Enter чтобы начать")
input()


# OpenWeatherMap
responce = requests.post(f"{W_URL}?q={W_CITY}&appid={W_API_KEY}&units=metric&lang=ru")
responce = responce.json()

weather = responce['weather'][0]['description']
temperature = responce['main']['temp']
humidity = responce['main']['humidity']
pressure = responce['main']['pressure']

print("Погода (OpenWeatherMap)")
print(f"Город: {W_CITY}\nПогода: {weather}\nТемпература: {temperature}C")
print(f"Давление: {pressure}hPa\nBлажность: {humidity}%\n")


# GetAmbee
headers = {
    'x-api-key': G_API_KEY
}
params = {
    "lat": G_LAT,
    "lng": G_LON,
    "units": "si"
}
responce = requests.get(G_URL, headers=headers, params=params)
responce = responce.json()

weather = responce['data']['summary']
temperature = responce['data']['temperature']
humidity = responce['data']['humidity']
pressure = responce['data']['pressure']

print("Погода (GetAmbee)")
print(f"Координаты: LAT={G_LAT}, LNG={G_LON}\nПогода: {weather}\nТемпература: {temperature}C")
print(f"Давление: {pressure}hPa\nBлажность: {humidity}%")