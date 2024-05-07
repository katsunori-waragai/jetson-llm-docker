#!/bin/bash
python3 -m pip install gdown
cd mmsegmentation
gdown --fuzzy -O work_dirs.zip https://drive.google.com/file/d/1DEJBeQ3cR1q7cjjzwDUIQVSoptT-y9U7/view?usp=drive_link
unzip work_dirs.zip
# rm work_dirs.zip