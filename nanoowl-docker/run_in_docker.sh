#!/bin/bash
# cd /root/torch2trt/
# python3 setup.py install
cd /root/nanoowl
python3 setup.py develop --user
mkdir -p data
python3 -m nanoowl.build_image_encoder_engine \
    data/owl_image_encoder_patch32.engine
