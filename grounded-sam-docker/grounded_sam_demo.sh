#!/bin/bash
case $# in
  2)
    name=$1
    prompt=$2;;
  *)
    echo "usage:$0 name text_prompt"
    exit 1;;
esac
  
echo python3 grounded_sam_demo.py   --config GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py \
   --grounded_checkpoint groundingdino_swint_ogc.pth \
   --sam_checkpoint sam_vit_h_4b8939.pth \
   --input_image ${name} \
   --output_dir "outputs" \
   --box_threshold 0.3   --text_threshold 0.25 \
   --text_prompt "${prompt}" \
   --device "cuda"

