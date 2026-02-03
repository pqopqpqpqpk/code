#################################################
#                                               #
#   python -m pip install opencv-python numpy   #
#                                               #
#################################################
import cv2
import numpy as np
import random
import os

input_file = '' # Your mp4 file
output_file = f"vhs_{os.path.splitext(input_file)[0]}.mp4"

cap = cv2.VideoCapture(input_file)
fps = cap.get(cv2.CAP_PROP_FPS)
# fps = 15
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

scale = 0.6
new_width = int(width * scale)
new_height = int(height * scale)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_file, fourcc, fps, (new_width, new_height))

dy = 2
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    #shaky
    if frame_count % 2 == 0:
        M = np.float32([[1, 0, 0], [0, 1, dy]])
    else:
        M = np.float32([[1, 0, 0], [0, 1, -dy]])
    frame = cv2.warpAffine(frame, M, (width, height))

    #down quality
    frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    #VHS nosie
    noise = np.random.randint(0, 50, (new_height, new_width, 1), dtype=np.uint8)
    noise = np.repeat(noise, 3, axis=2)
    frame = cv2.add(frame, noise)

    #RGB smearing
    b, g, r = cv2.split(frame)
    shift_val = random.randint(-2, 2)
    b = np.roll(b, shift_val, axis=1)
    g = np.roll(g, -shift_val, axis=0)
    r = np.roll(r, shift_val, axis=0)
    frame = cv2.merge([b, g, r])

    #horizontal line
    if random.random() < 0.1:
        y1 = random.randint(0, new_height - 2)
        thickness = random.randint(1, 3)
        frame[y1:y1+thickness, :] = frame[y1:y1+thickness, :] * 0.5 + np.random.randint(0, 128, (thickness, new_width, 3), dtype=np.uint8) * 0.5

    #blur
    frame = cv2.GaussianBlur(frame, (3, 3), 0)

    out.write(frame)
    frame_count += 1

cap.release()
out.release()
cv2.destroyAllWindows()
