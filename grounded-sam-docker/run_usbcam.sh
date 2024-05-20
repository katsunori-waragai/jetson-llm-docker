#!/bin/bash
echo "start grounded Dino"
python3 grounded_sam_movie.py   --config GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py \
   --grounded_checkpoint groundingdino_swint_ogc.pth \
   --sam_checkpoint sam_vit_h_4b8939.pth \
   --output_dir "outputs_captured" \
   --box_threshold 0.3   --text_threshold 0.25 \
   --text_prompt "arm . cup . keyboard . table . plate . bottle . PC . person" \
   --device "cuda"
