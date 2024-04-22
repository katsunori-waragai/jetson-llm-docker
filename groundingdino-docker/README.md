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



## trouble

name '_C' error

cuda のバージョンの問題
cuda-11.3 は GroundingDINO の記述
Jetson のは cuda-11.4


