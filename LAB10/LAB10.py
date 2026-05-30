from pathlib import Path
from faster_whisper import WhisperModel
from urllib.request import urlopen, urlretrieve
from PIL import Image
import sounddevice as sd
import numpy as np
import wave
import json
import random


DESC_FILENAME = "description.txt"
FOLDER = Path(__file__).resolve().parent  # Папка программы
TEMPFILE = "voice.wav"
USE_VOICE = 1
MODEL = "tiny"
PROMPT = ("Команды голосового управления на русском языке:"
          "случайный, эпизод, сохранить, показать, разрешение")
EXTENSIONS = {
    ".mp3", ".wav", ".m4a", ".flac", ".ogg", ".aac",
    ".mp4", ".mpeg", ".mpga", ".webm"
}
API = "https://rickandmortyapi.com/api/character/"


print("Лабораторная работа №10\nВыполнил: Коровин Матвей\nВариант 3")
print(f"Настройки: USE_VOICE={USE_VOICE}, MODEL={MODEL}")
print("Нажмите Enter чтобы начать. Введите что либо, чтобы вывести описание задачи")
use_description = input()
if use_description != "":
    try:
        with open(DESC_FILENAME, "r", encoding="utf-8") as file:
            text = file.read()
            print(text)
    except FileNotFoundError:
        print("Не удалось найти файл с описанием задачи")
        
        
def record_voice(filename):
    print("Нажми Enter, когда будешь готов сказать команду")
    input()
    print("Говори команду. Запись 4 секунды\n")
    try:
        audio = sd.rec(
            int(16000 * 4),
            samplerate=16000,
            channels=1,
            dtype=np.int16
        )
    except:
        raise RuntimeError("Не удалось подключить микрофон")
    sd.wait()
    with wave.open(filename, "wb") as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(16000)
        file.writeframes(audio.tobytes())


def obrabotka(command, id):
    print("Распознано: ", command)

    if ("лучай" in command) or ("СЛУЧАЙ" in command):
        id = np.random.randint(1, 826)
        with urlopen(f"https://rickandmortyapi.com/api/character/{id}") as response:
            data = json.loads(response.read().decode("utf-8"))
        print(f"Имя персонажа: {data["name"]}")

    elif ("эпизод" in command) or ("ЭПИЗОД" in command):
        with urlopen(f"https://rickandmortyapi.com/api/character/{id}") as response:
            data = json.loads(response.read().decode("utf-8"))
        if id:
            print(f"Эпизод появления: {data["episode"].rstrip("/").split("/")[-1]}")
        else:
            print("Для начала нужно выбрать персонажа")

    elif ("охран" in command) or ("СОХРАН" in command):
        with urlopen(f"https://rickandmortyapi.com/api/character/{id}") as response:
            data = json.loads(response.read().decode("utf-8"))
        if id:
            image_filename = FOLDER / f"{id}.jpeg"
            urlretrieve(data["image"], image_filename)
            print(f"Картинка для персонажа {data["name"]} сохранена в файл {image_filename}")
        else:
            print("Для начала нужно выбрать персонажа")

    elif ("оказ" in command) or ("ПОКАЗ" in command):
        if f"{id}.jpeg".exists():
            with Image.open(f"{id}.jpeg") as img:
                img.show()
            print("Картинка открыта")
        elif id:
            print("Для начала нужно сохранить картинку")
        else:
            print("Для начала нужно выбрать персонажа и сохранить картинку")

    elif ("азреш" in command) or ("СОХРАН" in command):
        if f"{id}.jpeg".exists():
            with Image.open(f"{id}.jpeg") as img:
                print(f"Разрешение картинки: {img.width}x{img.height}")
        elif id:
            print("Для начала нужно сохранить картинку")
        else:
            print("Для начала нужно выбрать персонажа и сохранить картинку")

    else:
        print("Команда не распознана")
        
    print()
    return id


if USE_VOICE != 0:
    id = 0
    while(1):
        record_voice(TEMPFILE)
        command = transcribe(TEMPFILE)
        obrabotka(command)
        TEMPFILE.unlink()
else:
    files = [ # Ищем файлы
        file for file in FOLDER.iterdir()
        if file.is_file() and file.suffix.lower() in EXTENSIONS
    ]
    files.sort()
    if not files:
        raise RuntimeError("Аудиофайлы не найдены")
    id = 0
    for file in files:
        command = transcribe(file)
        id = obrabotka(command, id)
