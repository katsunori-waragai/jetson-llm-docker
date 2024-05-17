#!/bin/bash
CAPTURED_FOLDER=captured_20240517
if [ ! -d ${CAPTURED_FOLDER} ]; then
  gdown --fuzzy --folder https://drive.google.com/drive/folders/1L1ZZPjTvswFxyNE5K75lAmMi-znHzfNx?usp=sharing
else
  echo already downloaded ${CAPTURED_FOLDER}
  echo ${CAPTURED_FOLDER}/*.jpg | sed 's/ /\n/g/'
fi
echo "start grounded Dino"
python3 grounded_sam_demo_my.py   --config GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py \
   --grounded_checkpoint groundingdino_swint_ogc.pth \
   --sam_checkpoint sam_vit_h_4b8939.pth \
   --image_dir ${CAPTURED_FOLDER} \
   --output_dir "outputs_captured" \
   --box_threshold 0.3   --text_threshold 0.25 \
   --text_prompt "arm . cup . keyboard . table " \
   --device "cuda"
