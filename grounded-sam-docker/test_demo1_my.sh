#!/bin/bash
python3 grounded_sam_demo_my.py \
   --image_dir assets/ \
   --output_dir "outputs" \
   --box_threshold 0.3   --text_threshold 0.25 \
   --text_prompt "bear " \
