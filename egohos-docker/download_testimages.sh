#!/bin/bash
python3 -m pip install gdown
if [ ! -f testimages.zip ]; then
  gdown --fuzzy -O testimages.zip https://drive.google.com/file/d/1G27in6x25VHdLVbftWv8ddt4kv_lyOmM/view?usp=sharing
fi
unzip testimages.zip
# rm testimages.zip
