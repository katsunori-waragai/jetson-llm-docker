Docker environment for grounding DINO

## GroundingDINO で何ができるのか

- https://github.com/IDEA-Research/GroundingDINO

## instruction
 
```
sh docker_build.sh
sh docker_run.sh
cd /root/GroundingDINO
sh 1_install_groundingDino.sh 
sh 2_reinstall-opencv.sh 
sh 3_download_weights.sh 
sh 4_detect.sh /root/data/dog.jpg
```

## instruction for webcam
usb カメラが /dev/video0として認識されていることを前提としています。
```commandline
$ sh 4_detect_webcam.sh
```
- コマンドの実行開始後に各種データファイルがダウンロードされるので、１０分程度時間がかかります。
- TensortRT化されていないので、推論の時間が余計にかかっています。

## demo/gradio_app.py
- 検出をweb　GUIで行うデモスクリプト。
前処理
```commandline
sed -s 's/pip /pip3 /g' demo/gradio_app.py 
```
- こうしておかないと、デフォルトのpythonがpython2.xのシステムではスクリプト中のpipがpython2.xの方に入ってしまう。
- gradio==3.50.2 として指定されている版を利用すること。
- それより新しい版では、仕様が変更になっているので、動作しない。


```commandline
python3 demo/gradio_app.py 
```

```commandline
Running on local URL: http://0.0.0.0:7579/
```
と表示されるので、ブラウザを開く。
##### トラブル
- 検出結果が描画されていない。

## GPU_ID
GPU_ID を取得するには、以下の情報を参照すること

https://forums.developer.nvidia.com/t/find-the-gpu-information/182768

## check point
- CUDA_HOME の設定 -> Dockerfile 中で ENV で設定した。
- {GPU_ID}の設定
- pythonのバージョンが循環import を生じない版であること。

## TODO
- 
- TensorRT化すること

## trouble

name '_C' error


https://github.com/IDEA-Research/Grounded-Segment-Anything/issues/275


cuda のバージョンの問題
cuda-11.3 は GroundingDINO の記述
Jetson のは cuda-11.4


