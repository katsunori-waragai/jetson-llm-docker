#!/bin/bash
python3 -m pip install gdown
gdown --fuzzy -O testimages.zip https://drive.google.com/file/d/1G27in6x25VHdLVbftWv8ddt4kv_lyOmM/view?usp=sharing
unzip testimages.zip
# rm testimages.zip