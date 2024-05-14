FROM nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3
RUN apt update
RUN apt install sudo
RUN apt install unzip
RUN cd /root/ && git clone https://github.com/owenzlz/EgoHOS
RUN cd /root/EgoHOS && sed -i '/^torch/d' requirements.txt
RUN cd /root/EgoHOS && python3 -m pip install -r requirements.txt
RUN cd /root/EgoHOS && python3 -m pip install -U openmim
RUN cd /root/EgoHOS && python3 -m pip install mmcv-full==1.6.0
RUN cd /root/EgoHOS/mmsegmentation && sed -i '/^torch/d' requirements/readthedocs.txt
RUN cd /root/EgoHOS/mmsegmentation && python3 -m pip install -v -e .
COPY download_*.sh /root/EgoHOS/
COPY my_pred_obj1_video.sh my_download_video.sh /root/EgoHOS/mmsegmentation/
COPY pred_twohands.sh /root/EgoHOS/mmsegmentation/
COPY *.py /root/EgoHOS/mmsegmentation/
ENV CUDA_HOME=/usr/local/cuda-11.4
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/cuda/bin
RUN python3 -m pip install gdown
RUN cd /root/EgoHOS && sh download_checkpoints.sh
RUN cd /root/EgoHOS && sh download_datasets.sh
RUN cd /root/EgoHOS && sh download_testimages.sh
RUN cd /root/EgoHOS && sh download_testvideos.sh
RUN cd /root/EgoHOS/mmsegmentation && sed -i 's/python /python3 /g' *.sh
RUN sed -i 's/python /python3 /g' /root/EgoHOS/mmsegmentation/predict_video.py
