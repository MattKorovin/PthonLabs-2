import cv2
import numpy as np


POINT = "ref-point.jpg"
MUHA = "fly64.png"

CAMERA = 0
BARRIER = 0.22 # см. desctiption2.txt

WIDTH = 640
HEIGHT = 480


cap = cv2.VideoCapture(CAMERA, cv2.CAP_DSHOW)
if not cap.isOpened():
    raise RuntimeError("Камера не открылась")
cap.release()

point = cv2.imread(POINT, cv2.IMREAD_GRAYSCALE)
if point is None:
    raise RuntimeError("Не удалось открыть изображение метки")

ys, xs = np.where(point < 245)
if len(xs) == 0 or len(ys) == 0:
    raise RuntimeError("На изображении метки не найдены тёмные области")


print("Лабораторная работа №7\nВыполнил: Коровин Матвей\nВариант 3")
print("Нажмите Enter чтобы начать")
input()

x1 = xs.min()
x2 = xs.max()
y1 = ys.min()
y2 = ys.max()
point = point[y1:y2, x1:x2]
templates = []
angles = [-20, -10, 0, 10, 20]

#point = cv2.GaussianBlur(point, (3, 3), 0)
point_edges = cv2.Canny(point, 50, 150)

for size in range(30, 221, 8):
    template = cv2.resize(point_edges, (size, size), interpolation=cv2.INTER_AREA)

    for angle in angles:
        center = (size // 2, size // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(template, matrix, (size, size), borderValue=0)

        if np.count_nonzero(rotated) > 20:
            templates.append((rotated, size, angle))

cap = cv2.VideoCapture(CAMERA, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
frame_id = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (WIDTH, HEIGHT), interpolation=cv2.INTER_LINEAR)

    target_size = 200
    target_x1 = WIDTH // 2 - target_size // 2
    target_y1 = HEIGHT // 2 - target_size // 2
    target_x2 = WIDTH // 2 + target_size // 2
    target_y2 = HEIGHT // 2 + target_size // 2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    edges = cv2.Canny(gray, 50, 150)

    best_score = -1
    best_pos = None
    best_size = None
    best_angle = None

    for template, size, angle in templates:
        if size >= edges.shape[0] or size >= edges.shape[1]:
            continue

        result = cv2.matchTemplate(edges, template, cv2.TM_CCOEFF_NORMED)
        _, score, _, pos = cv2.minMaxLoc(result)

        if score > best_score:
            best_score = score
            best_pos = pos
            best_size = size
            best_angle = angle

    cv2.rectangle(
        frame,
        (target_x1, target_y1),
        (target_x2, target_y2),
        (255, 0, 0),
        2
    )

    if best_score >= BARRIER:
        x, y = best_pos
        size = best_size

        cx = x + size // 2
        cy = y + size // 2

        in_target = target_x1 <= cx <= target_x2 and target_y1 <= cy <= target_y2

        marker_color = (0, 255, 0) if in_target else (0, 0, 255)
        text = "IN TARGET" if in_target else "OUT OF TARGET"

        cv2.rectangle(frame, (x, y), (x + size, y + size), marker_color, 2)
        cv2.circle(frame, (cx, cy), 4, marker_color, -1)

        cv2.putText(
            frame,
            f"{text}: x={cx} y={cy} score={best_score:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            marker_color,
            2,
            cv2.LINE_AA
        )

        cv2.putText(
            frame,
            f"angle={best_angle}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            marker_color,
            2,
            cv2.LINE_AA
        )

        if frame_id % 5 == 0:
            print(cx, cy, in_target, best_score)

    else:
        cv2.putText(
            frame,
            f"Marker not found, best={best_score:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
            cv2.LINE_AA
        )

    cv2.imshow("marker tracking", frame)

    cv2.imshow("edges", edges)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

    frame_id += 1