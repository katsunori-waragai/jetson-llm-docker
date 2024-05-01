#!/bin/bash
case $# in
  2)
    image_file=$1;
    tag=$2 ;;
  1)
    image_file=$1
    tag="dog"
    ;;
  *)
    echo "usage:" $0 "imagefile";
    exit ;;
esac

cd /root/GroundingDINO
CUDA_VISIBLE_DEVICES=0 \
python3 demo/inference_on_a_image.py \
-c groundingdino/config/GroundingDINO_SwinT_OGC.py \
-p weights/groundingdino_swint_ogc.pth \
-i ${image_file} \
-o outdir \
-t ${tag}
# [--cpu-only] # open it for cpu mode
