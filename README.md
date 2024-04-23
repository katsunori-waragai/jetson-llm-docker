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
- Each folder does not contain original repository.
- In some folders model are converted into TensorRT.

## Troubleshooting
- If you use torch2trt in Dockerfile, you must modify /etc/docker/daemon.json
```
"default-runtime": "nvidia",
```
is needed in the json file.

See 
https://github.com/NVIDIA-AI-IOT/torch2trt/issues/483
