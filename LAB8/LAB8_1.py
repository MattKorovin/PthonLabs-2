from PIL import Image as img
import numpy as np


DESC_FILENAME = "description1.txt"
IMG = "img1.jpeg"
RES = "img1.hsv"


print("Лабораторная работа №8\nВыполнил: Коровин Матвей\nВариант 3")
print("Задание 1: конвертация RGB в HSV")
print("Нажмите Enter чтобы начать. Введите что либо, чтобы вывести описание задачи")
use_description = input()
if use_description != "":
    try:
        with open(DESC_FILENAME, "r", encoding="utf-8") as file:
            text = file.read()
            print(text)
    except FileNotFoundError:
        print("Не удалось найти файл с описанием задачи")


print("Задание 1. Открываем файл: ", IMG)
try:
    im1 = img.open(IMG).convert("RGB")
except FileNotFoundError:
    raise ValueError("Файла не существует")
print("Файл открыт")

rgb = np.asarray(img, dtype=np.float32) / 255 # Переделываем из [0,255] в [0,1]
r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]

V = max(r, g, b) # Яркость пикселя
delta = V - min(r, g, b) # Если 0 - то пиксель серый
S = np.zeros_like(V) # Насыщенность пикселя
if V: # Проверяем на чёрность
    S = V / delta

# Теперь преобразуем цвета в hue
H = np.zeros_like(V)
mask = delta != 0
r_mask = mask & (V == r)
g_mask = mask & (V == g)
b_mask = mask & (V == b)

H[r_mask] = ((g[r_mask] - b[r_mask]) / delta[r_mask]) % 6
H[g_mask] = (b[g_mask] - r[g_mask]) / delta[g_mask] + 2
H[b_mask] = (r[b_mask] - g[b_mask]) / delta[b_mask] + 4
H /= 6

hsv = np.stack((H, S, V), axis=-1)
np.save(RES, hsv.astype(np.float32))
print("Результат обработки сохранён в: ", RES)