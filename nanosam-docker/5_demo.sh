#!/bin/bash
python3 examples/basic_usage.py \
    --image_encoder=data/resnet18_image_encoder.engine \
    --mask_decoder=data/mobile_sam_mask_decoder.engine

