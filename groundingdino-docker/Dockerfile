FROM nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3

ENV CUDA_HOME=/usr/local/cuda-11.4
RUN apt update
RUN apt install sudo
RUN apt-get install -y zip
RUN apt-get install -y nano
RUN python3 -m pip install -U pip
RUN python3 -m pip install wheel
RUN python3 -m pip uninstall -y opencv-python-headless
RUN python3 -m pip install opencv-python==3.4.18.65

RUN ldconfig

RUN if [ -f /usr/lib/aarch64-linux-gnu/tegra/libnvdla_compiler.so ] ; then echo "File exists"; else echo "File does not exist"; fi
RUN if [ -s /usr/lib/aarch64-linux-gnu/tegra/libnvdla_compiler.so ] ; then echo "File is not empty"; else echo "File is empty"; fi

ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/cuda/bin

RUN cd /root/ && git clone https://github.com/IDEA-Research/GroundingDINO.git
RUN cd /root/GroundingDINO && sed -i 's/^opencv-python.*$/opencv-python==3.4.18.65/' requirements.txt
RUN cd /root/GroundingDINO && sed -i '/opencv/d' environment.yaml 
RUN cd /root/GroundingDINO && python3 -m pip install -e .
RUN python3 -m pip uninstall -y opencv-python-headless
RUN python3 -m pip install opencv-python==3.4.18.65
RUN python3 -m pip uninstall gradio gradio_client
RUN python3 -m pip install gradio==3.50.2
RUN cd /root/GroundingDINO && mkdir -p weights
RUN cd /root/GroundingDINO/weights && wget -q https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth

COPY [1-9]_*.sh /root/GroundingDINO/
RUN cd /root/GroundingDINO && sed -i -e 's/"pip /"pip3 /g' -e 's/"python setup.py /"python3 setup.py /g' demo/gradio_app.py
COPY inference_on_a_movie.py /root/GroundingDINO/demo
