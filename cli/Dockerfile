FROM ubuntu:xenial

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 8AA7AF1F1091A5FD && \
    echo 'deb [arch=amd64] http://repo.sawtooth.me/ubuntu/bumper/stable xenial universe' >> /etc/apt/sources.list && \
    apt-get update

RUN apt-get install -y -q \
    python3-grpcio-tools \
    python3-requests \
    python3-setuptools \
    python3-sawtooth-sdk \
    python3-sawtooth-signing \
    python3-sawtooth-cli \
    iputils-ping \
    curl \
    telnet

#\
#    && /project/sawtooth_healthcare/bin/healthcare-protogen \
#    && cd /project/sawtooth_healthcare/processor/ \
#    && python3 setup.py clean --all \
#    && python3 setup.py

WORKDIR /project/sawtooth_healthcare

#ENV PATH $PATH:/project
#ENV PATH $PATH:/project/sawtooth_healthcare
ENV PATH $PATH:/project/sawtooth_healthcare/bin

#CMD ["echo", "$PATH"]
CMD echo "\033[0;32m--- Building cli ---\n\033[0m" \
    && init-healthcare-cli.sh
#    \
#    && healthcare-cli-python