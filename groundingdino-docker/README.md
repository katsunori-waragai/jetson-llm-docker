Docker environment for grounding DINO

## GroundingDINO で何ができるのか

- https://github.com/IDEA-Research/GroundingDINO

### purpose
- 自然言語で指定した記述にそって物体検出ができる。
- [文章で指定したものをなんでも検出できるAI Grounding DINO](https://qiita.com/john-rocky/items/2b62c70b606e3abc262f)

## instruction
 
```
sh docker_build.sh
sh docker_run.sh
cd /root/GroundingDINO
sh 4_detect.sh /root/data/dog.jpg
```

引数で指定した画像ファイルに対して -t "dog" のtagを与えられた内容について検出を実施しています。
結果は、-o で指定したディレクトリに書かれています。
- [x] 出力の確認

### note on Dockerfile
- opencv-python==3.4.18.65 
- gradio==3.50.2

## instruction for webcam
usb カメラが /dev/video0として認識されていることを前提としています。
```commandline
$ sh 4_detect_webcam.sh
```
- [x] USBカメラ入力、GUIへの結果の描画の確認。
- [x] -t "a woman with long hair" 
- コマンドの実行開始後に各種データファイルがダウンロードされるので、１０分程度時間がかかります。
- TensorRT化されていないので、推論の時間が余計にかかっています。

## demo/gradio_app.py
- 検出をweb　GUIで行うデモスクリプト。
前処理
```commandline
sed -i 's/pip /pip3 /g' demo/gradio_app.py 
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
- 
```
model loaded from /root/.cache/huggingface/hub/models--ShilongLiu--GroundingDINO/snapshots/a94c9b567a2a374598f05c584e96798a170c56fb/groundingdino_swint_ogc.pth 
 => _IncompatibleKeys(missing_keys=[], unexpected_keys=['label_enc.weight', 'bert.embeddings.position_ids'])
Traceback (most recent call last):
  File "demo/gradio_app.py", line 101, in <module>
    input_image = gr.Image(source='upload', type="pil")
  File "/usr/local/lib/python3.8/dist-packages/gradio/component_meta.py", line 159, in wrapper
    return fn(self, **kwargs)
TypeError: __init__() got an unexpected keyword argument 'source'
root@orin:~/GroundingDINO# 
```

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
- pytorchモデルのtensorRTモデルへの変換
- 推論スクリプトでのtensorRTモデルの指定

## trouble

name '_C' error


https://github.com/IDEA-Research/Grounded-Segment-Anything/issues/275


cuda のバージョンの問題
cuda-11.3 は GroundingDINO の記述
Jetson のは cuda-11.4


