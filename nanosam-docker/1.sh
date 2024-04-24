#!/bin/bash
python3 -m pip install timm
python3 -m pip install onnx
mkdir -v data
python3 -m nanosam.tools.export_sam_mask_decoder_onnx \
    --model-type=vit_t \
    --checkpoint=assets/mobile_sam.pt \
    --output=data/mobile_sam_mask_decoder.onnx

