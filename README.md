# Jetson LLM Docker
Jeston docker settings for LLMs

## Tested Environment
- NVIDIA Jetson AGX Orin
- JetPack5.1
- python3.8

## folders
- groundingdino-docker
  - https://github.com/IDEA-Research/GroundingDINO
  - open vocabulary object detection
- nanoowl-docker
  - https://github.com/NVIDIA-AI-IOT/nanoowl
  - open vocabulary object detection
- xmem-docker
  - https://github.com/hkchengrex/XMem
  - video segmentation
- yolov8-docker
  - https://github.com/ultralytics/ultralytics
  - object detection
- yolox-docker
  - https://github.com/Megvii-BaseDetection/YOLOX
  - object detection
## Note
- Each folder does not contain original repository.  git push --set-upstream origin feature/torch2trt-in-dockerfile
- In some folders model are converted into TensorRT.

## Troubleshooting
- If you use torch2trt in Dockerfile, you must modify /etc/docker/daemon.json
```
"default-runtime": "nvidia",
```
is needed in the json file.

See 
https://github.com/NVIDIA-AI-IOT/torch2trt/issues/483

## for disk space
- Jetson AGX Orin でのdocker の際にディスクスペースの枯渇を生じないように対策をとること。
  - microSD カードをext4 でフォーマットする。
  - それをmountするようにfstab に記載する。
  - /var/lib/docker の実体を増設したディスクにおくようにする。
  - そうすると元々のファイルシステムでの枯渇を予防できる。
  - [記事の例](https://qiita.com/nonbiri15/items/2a6b1fcc1a373e2b084c)

## todo
- TensortRT化されていないpytorch のモデルがあればtensorRT にモデルを変換して高速化すること。
- モデルファイルの中で、想定する入力画像の大きさが選べるときは、計算量を減らすモデルを利用することも視野に入れること。
- 推論の際に、実際にGPUを用いているかを確認すること
  - jtop 
  - https://www.fabshop.jp/jetson-nano-jtop/#google_vignette

