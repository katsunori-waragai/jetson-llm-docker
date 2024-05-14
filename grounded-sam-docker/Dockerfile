FROM nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3
ENV AM_I_DOCKER=False
ENV BUILD_WITH_CUDA=True

ENV CUDA_HOME=/usr/local/cuda-11.4
RUN apt update
RUN apt install sudo
RUN apt-get install -y zip
RUN apt-get install -y nano
RUN python3 -m pip install -U pip
RUN python3 -m pip install wheel
RUN python3 -m pip uninstall -y opencv-python-headless
RUN python3 -m pip install opencv-python==3.4.18.65
RUN python3 -m pip install -e segment_anything
RUN python3 -m pip install --no-build-isolation -e GroundingDINO
RUN python3 -m pip install --upgrade diffusers[torch]

RUN ldconfig

RUN if [ -f /usr/lib/aarch64-linux-gnu/tegra/libnvdla_compiler.so ] ; then echo "File exists"; else echo "File does not exist"; fi
RUN if [ -s /usr/lib/aarch64-linux-gnu/tegra/libnvdla_compiler.so ] ; then echo "File is not empty"; else echo "File is empty"; fi

ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/cuda/bin

RUN cd /root/ && git clone https://github.com/xinyu1205/recognize-anything.git
RUN cd /root/ && python3 -m pip install -r ./recognize-anything/requirements.txt
RUN cd /root/ && python3 pip install -e ./recognize-anything/
RUN python3 -m pip install opencv-python pycocotools matplotlib onnxruntime onnx ipykernel
