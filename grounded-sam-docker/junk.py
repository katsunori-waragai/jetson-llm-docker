import numpy as np
import cv2

color = (np.array([30/255, 144/255, 255/255, 0.6]))

h, w = 4800*2, 6400*2
mask = np.full((h, w, 1), 255, dtype=np.uint8)
t1 = cv2.getTickCount()
mask_image = mask * color.reshape(1, 1, -1)  # これが遅いのではなかろうか？
t2 = cv2.getTickCount()
print(f"{t2 - t1}")

t3 = cv2.getTickCount()
mask_image2 = np.full((h, w, 4), color, dtype=np.float32)
t4 = cv2.getTickCount()
print(f"{t4 - t3}")

