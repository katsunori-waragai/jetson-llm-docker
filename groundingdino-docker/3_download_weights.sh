#!/bin/sh
cd /root/GroundingDINO
if [ -f weights/groundingdino_swint_ogc.pth ]; then
    exit
fi
mkdir weights
cd weights
wget -q https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth
cd ..
