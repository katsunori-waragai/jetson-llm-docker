Docker environment for grounding DINO

## GroundingDINO で何ができるのか

- https://github.com/IDEA-Research/GroundingDINO

## instruction
 
```
sh docker_build.sh
sh docker_run.sh
cd /root/GroundingDINO
sh download_weights.sh
sh detect.sh /root/data/dog.jpg
```

##
GPU_ID を取得するには、以下の情報を参照すること

https://forums.developer.nvidia.com/t/find-the-gpu-information/182768

## trouble

name '_C' error

cuda のバージョンの問題
cuda-11.3 は GroundingDINO の記述
Jetson のは cuda-11.4


