#!/bin/sh
cd /root/GroundingDINO
python3 -m pip install -e .

python3 -m pip uninstall -y opencv-python
python3 -m pip uninstall -y opencv-python-headless
python3 -m pip install opencv-python==3.4.18.65

