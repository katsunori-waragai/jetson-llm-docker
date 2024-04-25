FROM nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3
RUN python3 -m pip install pillow --upgrade 
RUN python3 -m pip install timm
RUN python3 -m pip install onnx
RUN python3 -m pip install matplotlib
RUN python3 -m pip install pillow
RUN python3 -m pip install pycocotools
RUN python3 -m pip install transformers
RUN python3 -m pip install gdown

RUN cd /root/ && git clone https://github.com/NVIDIA-AI-IOT/torch2trt ;
RUN cd /root/torch2trt/ && python3 setup.py install --plugins
RUN cd /root/ && git clone https://github.com/NVIDIA-AI-IOT/trt_pose
RUN cd /root/trt_pose/ && python3 setup.py develop
RUN cd /root/ && git clone https://github.com/NVIDIA-AI-IOT/nanosam
RUN cd /root/nanosam/ && python3 setup.py develop

RUN cd /root/nanosam/ && mkdir -v data
RUN cd /root/nanosam/ && python3 -m nanosam.tools.export_sam_mask_decoder_onnx \
    --model-type=vit_t \
    --checkpoint=assets/mobile_sam.pt \
    --output=data/mobile_sam_mask_decoder.onnx

ENV PATH=$PATH:/usr/src/tensorrt/bin/

RUN cd /root/nanosam/ && trtexec \
    --onnx=data/mobile_sam_mask_decoder.onnx \
    --saveEngine=data/mobile_sam_mask_decoder.engine \
    --minShapes=point_coords:1x1x2,point_labels:1x1 \
    --optShapes=point_coords:1x1x2,point_labels:1x1 \
    --maxShapes=point_coords:1x10x2,point_labels:1x10

# download resnet18_image_encoder.onnx from Google Drive destnation is /root/nanosam/data
RUN cd /root/nanosam/data && \
	gdown --fuzzy https://drive.google.com/file/d/14-SsvoaTl-esC3JOzomHDnI9OGgdO2OR/view

# download densenet121_baseline_att_256x256_B_epoch_160.pth (used in TRT_pose)
RUN cd /root/nanosam/data && \
	gdown --fuzzy https://drive.google.com/open?id=13FkJkx7evQ1WwP54UmdiDXWyFMY1OxDU

RUN cd /root/nanosam/ && trtexec \
    --onnx=data/resnet18_image_encoder.onnx \
    --saveEngine=data/resnet18_image_encoder.engine \
    --fp16

RUN python3 -m pip uninstall opencv-python
RUN python3 -m pip uninstall opencv-python-headless
RUN python3 -m pip install opencv-python==3.4.18.65

COPY [1-9]*.sh /root/nanosam/
COPY my_*.py cvpil.py /root/nanosam/ 

