#FROM ubuntu:bionic
FROM debian:11
RUN apt-get -y --fix-missing update
RUN apt-get -y install wget apt-transport-https
RUN apt-get -y install python3 python3-dev python3-pip build-essential
RUN pip3 install --upgrade pip
RUN pip3 install datetime virtualenv requests tornado==4.5.3 textblob markdown igraph pyaes
RUN apt install schedtool -y
# for SOCK container engine
COPY sock2.py /

# Build python module in container to avoid depending on the host
COPY ol.c /
COPY setup.py /
RUN cd / && python3 setup.py build_ext --inplace && mv ol.*.so /ol.so
#COPY nltk_data /
COPY datain /
#COPY openpiton-readme.json /
# for Docker container engine
COPY server.py /
COPY spin /

CMD ["/spin"]
