#!/bin/bash
export ULTRALYSTICS=/usr/src/ultralytics
sudo docker run -it --rm --net=host --runtime nvidia -e DISPLAY=$DISPLAY \
	-v ~/github/yolov8-docker/runs:${ULTRALYSTICS}/runs \
	-v ~/github/yolov8-docker:${ULTRALYSTICS}/yolov8-docker \
	--device /dev/bus/usb \
	--device /dev/video0:/dev/video0:mwr \
	-v /tmp/.X11-unix/:/tmp/.X11-unix yolov8:100
 

