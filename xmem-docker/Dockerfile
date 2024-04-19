FROM nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3
RUN apt update
RUN apt install sudo
RUN apt-get install -y zip
RUN apt-get install -y build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
RUN apt-get install -y libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libdc1394-22-dev
RUN apt-get install -y libv4l-dev v4l-utils qv4l2

RUN apt-get install -y libxcb-cursor-dev
RUN apt-get install -y libxcb-cursor0

RUN python3 -m pip install -U pip
RUN python3 -m pip install progressbar
RUN cd /root && git clone https://github.com/hkchengrex/XMem.git
RUN cd /root/XMem && python3 -m pip install -r requirements.txt ;  python3 -m pip install -r requirements_demo.txt
RUN cd /root/XMem && sh ./scripts/download_models_demo.sh
