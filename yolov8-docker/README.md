# yolov8-docker
yolov8 docker
yolov8 を用いたセグメンテーション
Jetson AGX Orin Dveloper Kit

## github [ultralytics](https://github.com/ultralytics/ultralytics)
[Dockerfile-jetson](https://github.com/ultralytics/ultralytics/blob/main/docker/Dockerfile-jetson)

## 制限事項
- AGPL3 のライセンスなので、実機での運用には使わない。
- あくまで、現状の検出、セグメンテーション、ポーズ推定がどうなっているのかを見るための利用。

## 手順
```
$ sudo bash docker_build.sh
$ sudo bash docker_run.sh
# pip install ultralytics

# yolo predict model=yolov8n.pt source='https://ultralytics.com/images/bus.jpg'

# yolo segment predict model=yolov8s-seg.pt source='https://ultralytics.com/images/bus.jpg' conf=0.25 iou=0.45 save=True

# python3 segment_sample.py
```

segment_sample_imshow.py　　# cv2.VideoCapture(0) を用いた動作例
pose_sample_imshow.py　　# cv2.VideoCapture(0) を用いた動作例

### tracking
https://docs.ultralytics.com/ja/modes/track/#__tabbed_1_2
```
yolo track model=yolov8n.pt source="https://youtu.be/LNwODJXcvt4"  # Official Detect model
```

### 保存先
`Results saved to /usr/src/ultralytics/runs/segment/predict`

### yolo command usage
```
# yolo help

    Arguments received: ['yolo', 'help']. Ultralytics 'yolo' commands use the following syntax:

        yolo TASK MODE ARGS

        Where   TASK (optional) is one of ('detect', 'segment', 'classify', 'pose', 'obb')
                MODE (required) is one of ('train', 'val', 'predict', 'export', 'track', 'benchmark')
                ARGS (optional) are any number of custom 'arg=value' pairs like 'imgsz=320' that override defaults.
                    See all ARGS at https://docs.ultralytics.com/usage/cfg or with 'yolo cfg'

    1. Train a detection model for 10 epochs with an initial learning_rate of 0.01
        yolo train data=coco128.yaml model=yolov8n.pt epochs=10 lr0=0.01

    2. Predict a YouTube video using a pretrained segmentation model at image size 320:
        yolo predict model=yolov8n-seg.pt source='https://youtu.be/LNwODJXcvt4' imgsz=320

    3. Val a pretrained detection model at batch-size 1 and image size 640:
        yolo val model=yolov8n.pt data=coco128.yaml batch=1 imgsz=640

    4. Export a YOLOv8n classification model to ONNX format at image size 224 by 128 (no TASK required)
        yolo export model=yolov8n-cls.pt format=onnx imgsz=224,128

    6. Explore your datasets using semantic search and SQL with a simple GUI powered by Ultralytics Explorer API
        yolo explorer

    5. Run special commands:
        yolo help
        yolo checks
        yolo version
        yolo settings
        yolo copy-cfg
        yolo cfg

    Docs: https://docs.ultralytics.com
    Community: https://community.ultralytics.com
    GitHub: https://github.com/ultralytics/ultralytics```
```

- 例示にあるように、web上のyoutube動画をそのまま入力にすることができる。
 save=True を付けると、avi形式での動画が保存される。


## todo
- カメラ入力に対するsegmentation の実施
- その画面への表示
- TensorRTの利用
