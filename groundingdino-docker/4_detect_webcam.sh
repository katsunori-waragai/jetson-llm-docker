#!/bin/bash
case $# in
  2)
    cameraid=$1;
    tag="$2" ;;
  1)
    cameraid=$1
    tag="head . face . eye . hand"
    ;;
  *)
    echo "usage:" $0 "cameraid [tag_string]";
    echo "example" $0 "0 [head . face . eye . hand]";
    exit ;;
esac


cd /root/GroundingDINO
CUDA_VISIBLE_DEVICES=0 \
python3 demo/inference_on_a_movie.py \
-c groundingdino/config/GroundingDINO_SwinT_OGC.py \
-p weights/groundingdino_swint_ogc.pth \
-i ${cameraid} \
-o outdir \
-t "${tag}"
# [--cpu-only] # open it for cpu mode
