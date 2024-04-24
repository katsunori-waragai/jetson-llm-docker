#!/bin/bash
export PATH=$PATH:/usr/src/tensorrt/bin/

trtexec \
    --onnx=data/mobile_sam_mask_decoder.onnx \
    --saveEngine=data/mobile_sam_mask_decoder.engine \
    --minShapes=point_coords:1x1x2,point_labels:1x1 \
    --optShapes=point_coords:1x1x2,point_labels:1x1 \
    --maxShapes=point_coords:1x10x2,point_labels:1x10
