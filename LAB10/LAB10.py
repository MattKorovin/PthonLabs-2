from pathlib import Path
from faster_whisper import WhisperModel
from urllib.request import urlopen, Request
from PIL import Image
import sounddevice as sd
import numpy as np
import wave
import json


DESC_FILENAME = "description.txt"
USE_VOICE = 1 # Если 0 - то анализирует готовые аудиофайлы

# Без этого не работало
FOLDER = Path(__file__).resolve().parent  # Папка программы
TEMPFILE = FOLDER / "voice.wav"

MODEL = "tiny"
PROMPT = "Дай точную расшифорвку на русском языке: случайный, эпизод, сохранить, показать, разрешение"
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
    print("Запись завершена!",end=" ")
    with wave.open(str(filename), "wb") as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(16000)
        file.writeframes(audio.tobytes())


def transcribe(filename):
    segments, info = WhisperModel(MODEL).transcribe(
        str(TEMPFILE),
        language="ru",
        task="transcribe",
        initial_prompt=PROMPT
    )
    text = " ".join(segment.text.strip() for segment in segments).strip()
    print(f"Распознано: {text}")
    return text.lower().replace("ё", "е")


def get_json(url):
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))

def download_file(url, id):
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request) as response:
        data = response.read()
    with open(FOLDER / f"{id}.jpeg", "wb") as file:
        file.write(data)


def obrabotka(command, id):
    if ("лучай" in command) or ("СЛУЧАЙ" in command):
        # Всего записей на сайте (на момент создания лабы) - 826
        id = np.random.randint(1, 826)
        data = get_json(f"{API}{id}")
        print(f"Имя персонажа: {data["name"]}")

    elif ("эпизод" in command) or ("ЭПИЗОД" in command):
        data = get_json(f"{API}{id}")
        if id:
            print(f"Эпизод появления: {data["episode"][0].rstrip("/").split("/")[-1]}")
        else:
            print("Для начала нужно выбрать персонажа")

    elif ("охран" in command) or ("СОХРАН" in command):
        data = get_json(f"{API}{id}")
        if id:
            download_file(data["image"], id)
            print(f"Картинка для персонажа {data["name"]} сохранена в файл {id}.jpeg")
        else:
            print("Для начала нужно выбрать персонажа")

    elif ("оказ" in command) or ("ПОКАЗ" in command):
        if (FOLDER / f"{id}.jpeg").exists():
            with Image.open(f"{id}.jpeg") as img:
                img.show()
            print("Картинка открыта")
        elif id:
            print("Для начала нужно сохранить картинку")
        else:
            print("Для начала нужно выбрать персонажа и сохранить картинку")

    elif ("азреш" in command) or ("СОХРАН" in command):
        if (FOLDER / f"{id}.jpeg").exists():
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
        id = obrabotka(command, id)
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