import io

import requests
import os
from dotenv import load_dotenv
from urllib.request import urlopen, Request
import tkinter as tk
from PIL import Image, ImageTk

load_dotenv()
DESC_FILENAME="description.txt"

# OpenWeatherMap
W_API_KEY = os.getenv('W_API_KEY')
W_URL = "https://api.openweathermap.org/data/2.5/weather"
W_CITY = "Dronten"

# GetAmbee
G_API_KEY = os.getenv("G_API_KEY")
G_URL = "https://api.ambeedata.com/disasters/latest/by-lat-lng"
G_LAT = 52.532079
G_LON = 5.727108

# Котики :3
C_URL = "https://cataas.com/cat?type=square"

def download_file():
    request = Request(C_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request) as response:
        data = response.read()
    return data

def run():
    temp = Image.open(io.BytesIO(download_file()))
    temp = temp.resize((800, 800), Image.LANCZOS) # Растягиваем до 800х800
    background = ImageTk.PhotoImage(temp)
    canvas.itemconfig(background_image, image=background)
    canvas.image = background


print("Лабораторная работа №7\nВыполнил: Коровин Матвей\nВариант 3")
print("Нажмите Enter чтобы начать. Введите что либо, чтобы вывести описание задачи")
use_description = input()
if use_description != "":
    try:
        with open(DESC_FILENAME, "r", encoding="utf-8") as file:
            text = file.read()
            print(text)
    except FileNotFoundError:
        print("Не удалось найти файл с описанием задачи")


# OpenWeatherMap
responce = requests.post(f"{W_URL}?q={W_CITY}&appid={W_API_KEY}&units=metric&lang=ru")
responce = responce.json()

weather = responce['weather'][0]['description']
temperature = responce['main']['temp']
humidity = responce['main']['humidity']
pressure = responce['main']['pressure']

print("Задание 1. Погода (OpenWeatherMap)")
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
responce = (responce.json())['result']
N = len(responce)

print("Задание 2. Катаклизмы (GetAmbee)")
print(f"Координаты: LAT={G_LAT}, LNG={G_LON}")
print(f"По координатам найдено {N} катаклизмов", end="")
if(N):
    print(":")
    for i in range(N):
        print(f"\nКатаклизм {i+1}:")
        print(f"Название катаклизма: {responce[i]['event_name']}")
        print(f"Уровень серьёзности: {responce[i]['proximity_severity_level']}")
        print(f"Уровень тревоги: {responce[i]['default_alert_levels']}")
        print(f"Ожидаемая дата окончания (гггг-мм-дд): {responce[i]['estimated_end_date']}")
else:
    print(".")


print("\nЗадание 3. Генератор котиков")
print("Нажмите Enter, чтобы открыть генератор")
input()

window = tk.Tk() # Делаем начальные параметры окна
window.geometry('800x800')
window.resizable(False, False)
canvas = tk.Canvas(window, width=800, height=800)
canvas.pack()

temp = Image.open(io.BytesIO(download_file()))
temp = temp.resize((800, 800), Image.LANCZOS) # Растягиваем до 800х800
background = ImageTk.PhotoImage(temp)
background_image = canvas.create_image(0, 0, image=background, anchor="nw")
button = tk.Button(window, text="Следующий", font=("Arial", 16), command=run)

button_canvas = canvas.create_window(400, 700, window=button)
window.mainloop()