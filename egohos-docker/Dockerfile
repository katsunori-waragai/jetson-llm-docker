FROM nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3
RUN apt update
RUN apt install sudo
RUN apt install unzip
RUN cd /root/ && git clone https://github.com/owenzlz/EgoHOS
RUN cd /root/EgoHOS && python3 -m pip install -r requirements.txt
RUN cd /root/EgoHOS && python3 -m pip install -U openmim
RUN cd /root/EgoHOS && python3 -m pip install mmcv-full==1.6.0
RUN cd /root/EgoHOS/mmsegmentation && python3 -m pip install -v -e .
RUN cd /root/EgoHOS && COPY download_*.sh .
