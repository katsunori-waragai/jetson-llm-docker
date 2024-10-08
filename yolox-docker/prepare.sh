#!/bin/sh
cd /root/YOLOX
export TRTMODEL_S=YOLOX_outputs/yolox_s/model_trt.pth
if [ ! -f ${TRTMODEL_S} ]; then
	python3 tools/trt.py -n yolox-s -c yolox_s.pth
fi

export TRTMODEL_TINY=YOLOX_outputs/yolox_tiny/model_trt.pth
if [ ! -f ${TRTMODEL_TINY} ]; then
	python3 tools/trt.py -n yolox-tiny -c yolox_tiny.pth
fi

