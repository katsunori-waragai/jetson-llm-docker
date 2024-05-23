#!/bin/bash
mkdir -p image_hq
cd image_hq && wget https://github.com/IDEA-Research/detrex-storage/releases/download/grounded-sam-storage/sam_hq_demo_image.png
cd ..

export CUDA_VISIBLE_DEVICES=0
python3 gsam.py \
   --use_sam_hq \
   --image_dir image_hq \
   --output_dir "outputs_image_hq" \
   --box_threshold 0.3   --text_threshold 0.25 \
   --text_prompt "arm . cup . keyboard . table . chair" \
