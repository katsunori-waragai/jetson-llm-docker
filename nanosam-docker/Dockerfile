FROM nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3
RUN python3 -m pip install pillow --upgrade 

RUN cd /root/ && git clone https://github.com/NVIDIA-AI-IOT/torch2trt ;
RUN cd /root/torch2trt/ && python3 setup.py install --plugins
RUN cd /root/ && git clone https://github.com/NVIDIA-AI-IOT/trt_pose
RUN cd /root/trt_pose/ && python3 setup.py develop
RUN cd /root/ && git clone https://github.com/NVIDIA-AI-IOT/nanosam
RUN cd /root/nanosam/ && python3 setup.py develop

COPY [1-9]*.sh /root/nanosam/
