#!/bin/bash
if [ ! -d captured_20240517 ]; then
  gdown --fuzzy --folder https://drive.google.com/drive/folders/1L1ZZPjTvswFxyNE5K75lAmMi-znHzfNx?usp=sharing
fi
python3 grounded_sam_demo_my.py   --config GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py \
   --grounded_checkpoint groundingdino_swint_ogc.pth \
   --sam_checkpoint sam_vit_h_4b8939.pth \
   --image_dir captured_20240517 \
   --output_dir "outputs_captured" \
   --box_threshold 0.3   --text_threshold 0.25 \
   --text_prompt "arm . cup . keyboard . table " \
   --device "cuda"
