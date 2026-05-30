import cv2
import numpy as np


DESC_FILENAME = "description2.txt"
IMG = "img2.jpg"
CAM = 0


print("Лабораторная работа №8\nВыполнил: Коровин Матвей\nВариант 3")
print("Задание 2: отслеживание маркера")
print("Нажмите Enter чтобы начать. Введите что либо, чтобы вывести описание задачи")
use_description = input()
if use_description != "":
    try:
        with open(DESC_FILENAME, "r", encoding="utf-8") as file:
            text = file.read()
            print(text)
    except FileNotFoundError:
        print("Не удалось найти файл с описанием задачи")


# Камера откройся!!!
cap = cv2.VideoCapture(CAM, cv2.CAP_DSHOW)
if cap.isOpened():
    print(f"Открыта камера {CAM}")
else:
    print(f"Не удалось открыть камеру {CAM}. Открываем другую...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if cap.isOpened():
        print(f"Открыта камера 0")
    else:
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        if cap.isOpened():
            print("Открыта камера 1")
        else:
            raise RuntimeError("Не удалось открыть камеру. Попробуйте"
                               "сменить камеру или запустить"
                               "программу от имени администратора")
