#!/bin/bash
trtexec \
    --onnx=data/resnet18_image_encoder.onnx \
    --saveEngine=data/resnet18_image_encoder.engine \
    --fp16

