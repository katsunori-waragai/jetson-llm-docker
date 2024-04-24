FROM nvcr.io/nvidia/pytorch:23.01-py3
RUN python3 -m pip install pillow --upgrade 

RUN cd /root/ && git clone https://github.com/NVIDIA-AI-IOT/torch2trt ;
RUN cd /root/torch2trt && python3 setup.py install --plugins
RUN cd /root/ && git clone https://github.com/NVIDIA-AI-IOT/trt_pose
RUN cd /root/trt_pose && python3 setup.py develop
