# Jetson LLM Docker
Jeston docker settings for LLMs(Large Language Models)

## Tested Environment
- NVIDIA Jetson AGX Orin
- JetPack5.1
- python3.8

## folders
- egoHOS
  - https://github.com/owenzlz/EgoHOS
  - Fine-Grained Egocentric Hand-Object Segmentation
  - 左腕・右腕のsegmenation、1st, 2nd order interaction object の検出 
- groundingdino-docker
  - https://github.com/IDEA-Research/GroundingDINO
  - open vocabulary object detection
  - 検出対象の制約のない言葉を指定する物体検出
  - text prompt によって指定されたものを検出する。
  - “a woman with long hair” といった指定で検出ができる。
- nanoowl-docker
  - https://github.com/NVIDIA-AI-IOT/nanoowl
  - open vocabulary object detection
- nanosam-docker
  - https://github.com/NVIDIA-AI-IOT/nanosam
  - Segment Anything for Jetson 
  - nanosam/examples/demo_pose_tshirt.py　Tシャツのセグメンテーション
- xmem-docker
  - https://github.com/hkchengrex/XMem
  - video segmentation
- yolov8-docker
  - https://github.com/ultralytics/ultralytics
  - object detection
- yolox-docker
  - https://github.com/Megvii-BaseDetection/YOLOX
  - object detection
## policy in this repository
- Each folder does NOT contain original repository. 
- In some folders models are converted into TensorRT.
	*.engine

## for disk space
複数のdocker環境を使い分ける際には、たくさんのディスクスペースをキャッシュとして使います。
Jetson AGX Orin のディスクスペースでは、docker のキャッシュが収まり切らなくなります。
そこで、microSDカードを用いて、その領域にdockerのキャッシュをおくように変更することで、キャッシュが有効な状態でも、ルートのファイルシステムでのディスクスペースの枯渇を防ぐことができます。

- Jetson AGX Orin でのdocker の際にディスクスペースの枯渇を生じないように対策をとること。
  - microSD カードをext4 でフォーマットする。
  - それをmountするようにfstab に記載する。
  - /var/lib/docker の実体を増設したディスクにおくようにする。
  - そうすると元々のファイルシステムでの枯渇を予防できる。
  - [記事の例](https://qiita.com/nonbiri15/items/2a6b1fcc1a373e2b084c)

## model conversion by Torch2TRT
- Pytorch based models were converted to trt models using torch2trt.
- The conversion is executed in Dockerfile.
- This takes more than 10 minitues. Be patient.


## Troubleshooting
- If you execute `torch2trt` in `Dockerfile`, you must modify `/etc/docker/daemon.json`
```
"default-runtime": "nvidia",
```
is needed in the json file.

See 
https://github.com/NVIDIA-AI-IOT/torch2trt/issues/483

  
## todo
- TensortRT化されていないpytorch のモデルがあればtensorRT にモデルを変換して高速化すること。
- モデルファイルの中で、想定する入力画像の大きさが選べるときは、計算量を減らすモデルを利用することも視野に入れること。
- 推論の際に、実際にGPUを用いているかを確認すること
  - jtop 
  - https://www.fabshop.jp/jetson-nano-jtop/#google_vignette

## Network requirement
- Inference script downloads model files in execution.

