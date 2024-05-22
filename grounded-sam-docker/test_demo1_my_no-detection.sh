#!/bin/bash
python3 grounded_sam_demo_my.py \
   --input_image assets/demo1.jpg \
   --output_dir "outputs" \
   --box_threshold 0.3   --text_threshold 0.25 \
   --text_prompt "cup " \
