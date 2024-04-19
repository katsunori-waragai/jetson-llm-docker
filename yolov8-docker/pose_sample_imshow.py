"""
pip3 install "opencv-python<=3.4.18.65"
"""

from pathlib import Path
import os
import cv2

def read_result_image():
	files = list(Path("runs/pose/").glob("predict*/*.jpg"))
	files.sort(key=os.path.getmtime)
	print(f"{files=}")
	img = cv2.imread(str(files[-1]))
	return img

from ultralytics import YOLO
# モデルの生成。モデルは自動でダウンロードされます。
model = YOLO("yolov8n-pose.pt")
# 推論実行
if 0:
	src = "https://ultralytics.com/images/bus.jpg"
	results = model(src, save=True)
else:
	capture = cv2.VideoCapture(0)
	_, img = capture.read()
	results = model(source=img, save=True) 

img = read_result_image()
print(f"{img=}")
cv2.imshow("result", img)
cv2.waitKey(-1)


