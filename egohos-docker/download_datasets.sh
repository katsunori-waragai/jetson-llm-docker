#!/bin/bash
pip3 install gdown
mkdir -p data
cd data
if [ ! -f egohos_dataset.zip ]; then
  gdown --fuzzy -O egohos_dataset.zip https://drive.google.com/file/d/1sk0TVEhZESNF67OW3fz9D5coqpIWkwuK/view?usp=sharing
fi
unzip egohos_dataset.zip
# rm egohos_dataset.zip
