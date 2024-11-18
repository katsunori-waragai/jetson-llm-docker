FROM dustynv/nanosam:r36.2.0
ENV PATH=$PATH:/usr/src/tensorrt/bin/

COPY [1-9]*.sh /opt/nanosam/
COPY my_*.py cvpil.py /opt/nanosam/

# image file viwewer
RUN apt-get update
RUN apt-get install -y eog

