#!/bin/bash
export GIT_ROOT=$(cd $(dirname $0)/.. ; pwd)
sudo docker run -it --rm --net=host --runtime nvidia -e DISPLAY=$DISPLAY \
        --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 \
	--device /dev/bus/usb \
	--device /dev/video0:/dev/video0:mwr \
	-v /tmp/.X11-unix/:/tmp/.X11-unix nanosam:100
 
