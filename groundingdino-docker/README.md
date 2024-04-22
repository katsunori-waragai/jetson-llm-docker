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

## GPU_ID
GPU_ID を取得するには、以下の情報を参照すること

https://forums.developer.nvidia.com/t/find-the-gpu-information/182768

## check point
- CUDA_HOME の設定 -> Dockerfile 中で ENV で設定した。
- {GPU_ID}の設定
- pythonのバージョンが循環import を生じない版であること。

## trouble

name '_C' error


https://github.com/IDEA-Research/Grounded-Segment-Anything/issues/275


cuda のバージョンの問題
cuda-11.3 は GroundingDINO の記述
Jetson のは cuda-11.4


