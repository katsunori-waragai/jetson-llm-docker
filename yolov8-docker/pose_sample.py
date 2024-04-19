from ultralytics import YOLO
# モデルの生成。モデルは自動でダウンロードされます。
model = YOLO("yolov8n-pose.pt")
# 推論実行
results = model("https://ultralytics.com/images/bus.jpg", save=True)

