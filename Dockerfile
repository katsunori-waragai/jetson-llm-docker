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
RUN apt-get install -y nvidia-container-runtime nvidia-container-toolkit nvidia-container
RUN python3 -m pip install -U pip
RUN python3 -m pip install wheel
RUN python3 -m pip install loguru tqdm thop ninja tabulate
RUN python3 -m pip install pycocotools
RUN python3 -m pip install opencv-python==3.4.18.65
RUN python3 -m pip install transformers
RUN python3 -m pip install onnx
RUN python3 -m pip install openai-clip
RUN python3 -m pip install aiohttp
# RUN python3 -m pip install --upgrade tensorrt
RUN python3 -m pip install nvidia-pyindex
# RUN python3 -m pip install nvidia-tensorrt==8.4.1.5
RUN python3 -m pip install "tensorrt<=8.6"

RUN ldconfig

RUN python3 -c "import onnx"
RUN if [ -f /usr/lib/aarch64-linux-gnu/tegra/libnvdla_compiler.so ] ; then echo "File exists"; else echo "File does not exist"; fi
RUN if [ -s /usr/lib/aarch64-linux-gnu/tegra/libnvdla_compiler.so ] ; then echo "File is not empty"; else echo "File is empty"; fi
# RUN python3 -c "import tensorrt"
# torch2trt
RUN cd /root/ && git clone https://github.com/NVIDIA-AI-IOT/torch2trt ;
# RUN cd /root/torch2trt; python3 setup.py install

RUN cd /root && git clone https://github.com/NVIDIA-AI-IOT/nanoowl ; cd nanoowl cd ; python3 setup.py develop --user



