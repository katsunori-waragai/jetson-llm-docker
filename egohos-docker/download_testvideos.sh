#!/bin/bash
python3 -m pip install gdown
if [ ! -f testvideos.zip ]; then
  gdown --fuzzy -O testvideos.zip https://drive.google.com/file/d/1pxm-sT9idU3oa1HC6SY4vrGVvJw_ElVO/view?usp=sharing
fi
unzip testvideos.zip
# rm testvideos.zip
