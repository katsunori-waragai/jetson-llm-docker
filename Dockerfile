FROM nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3
RUN apt update
RUN apt install sudo
RUN apt-get install -y zip
RUN apt-get install -y build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
RUN apt-get install -y libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libdc1394-22-dev
RUN apt-get install -y libv4l-dev v4l-utils qv4l2
RUN apt-get install -y curl
RUN apt-get install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
RUN apt-get install -y tensorrt nvidia-tensorrt python3-libnvinfer
RUN apt-get install -y cuda-toolkit-11.4
RUN apt-get install -y libnvidia-container-tools libnvidia-container0 libnvidia-container1
# RUN apt-get install -y nvidia-container-csv-cuda nvidia-container-csv-cudnn 
# RUN apt-get install -y nvidia-container-csv-tensorrt
# RUN apt-get install -y nvidia-container-csv-visionworks
RUN apt-get install -y nvidia-container-runtime nvidia-container-toolkit nvidia-container
RUN python3 -m pip install -U pip
RUN python3 -m pip install loguru tqdm thop ninja tabulate
RUN python3 -m pip install pycocotools


RUN python3 -m pip install opencv-python==3.4.18.65

RUN ldconfig
# torch2trt
RUN cd /root/ && git clone https://github.com/NVIDIA-AI-IOT/torch2trt ;
# RUN cd /root/torch2trt; python3 setup.py install

# RUN python3 -m pip install transformers
# RUN cd /root && git clone https://github.com/NVIDIA-AI-IOT/nanoowl ; cd nanoowl cd ; python3 setup.py develop --user

# RUN cd /root/YOLOX && python3 tools/trt.py -n yolox-s -c yolox_s.pth
