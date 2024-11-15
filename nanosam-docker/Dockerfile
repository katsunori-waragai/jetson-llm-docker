FROM dustynv/nanosam:r36.2.0
ENV PATH=$PATH:/usr/src/tensorrt/bin/

COPY [1-9]*.sh /root/nanosam/
COPY my_*.py cvpil.py /root/nanosam/ 

# image file viwewer
RUN apt-get update
RUN apt-get install -y eog

