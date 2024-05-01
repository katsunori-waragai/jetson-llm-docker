#!/bin/bash
sed -i 's/"pip /"pip3 /g' demo/gradio_app.py
sed -i 's/"python setup.py /"python3 setup.py /g' demo/gradio_app.py
