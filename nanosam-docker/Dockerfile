FROM dustynv/nanosam:r36.2.0
ENV PATH=$PATH:/usr/src/tensorrt/bin/
# RUN cd /root/nanosam/ && trtexec \
#     --onnx=data/resnet18_image_encoder.onnx \
#     --saveEngine=data/resnet18_image_encoder.engine \
#     --fp16

# RUN python3 -m pip uninstall opencv-python
# RUN python3 -m pip uninstall opencv-python-headless
# RUN python3 -m pip install opencv-python==3.4.18.65

COPY [1-9]*.sh /root/nanosam/
COPY my_*.py cvpil.py /root/nanosam/ 

# image file viwewer
RUN apt-get update
RUN apt-get install -y eog

