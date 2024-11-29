#!/bin/bash
sudo docker run -it --rm --net=host --runtime nvidia -e DISPLAY=$DISPLAY \
	--privileged \
	-v ${HOME}/github/zed-sdk/:/usr/local/zed/zed-sdk \
	--device /dev/bus/usb \
	--device /dev/video0:/dev/video0:mwr \
	-v /tmp/.X11-unix/:/tmp/.X11-unix zed-docker:100
