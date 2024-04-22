#!/bin/bash
case $# in
  1)
    echo "1" ;;
  *)
    echo "usage:" $0 "imagefile";
    exit ;;
esac

cd /root/GroundingDINO
# CUDA_VISIBLE_DEVICES={GPU ID} 
python3 demo/inference_on_a_image.py \
-c groundingdino/config/GroundingDINO_SwinT_OGC.py \
-p weights/groundingdino_swint_ogc.pth \
-i $1 \
-o outdir \
-t "dog"
# [--cpu-only] # open it for cpu mode
