# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

# This Dockerfile is for running protogen, lint, and unit-tests

FROM ubuntu:xenial

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 8AA7AF1F1091A5FD && \
    echo 'deb [arch=amd64] http://repo.sawtooth.me/ubuntu/bumper/stable xenial universe' >> /etc/apt/sources.list && \
    apt-get update --fix-missing

RUN apt-get install --fix-missing -y --allow-unauthenticated -q \
    locales \
    python3-pip \
    python3-sawtooth-sdk \
    python3-setuptools \
    python3-sawtooth-rest-api \
    python3-grpcio-tools \
    python3-sawtooth-cli \
    python3-sawtooth-signing \
#        cron-apt \
    iputils-ping \
    curl \
    telnet

RUN locale-gen en_US.UTF-8
#RUN curl -sL https://deb.nodesource.com/setup_6.x | bash - \
#    && apt-get install -y nodejs

RUN pip3 install \
#    pylint==1.8.1 \
#    pycodestyle==2.3.1 \
#    grpcio-
#    \
#    nose2==0.7.2 \
#    bcrypt \
#    pycrypto \
#    rethinkdb \
    sanic==19.03.1 \
    sanic_cors
#    \
#    itsdangerous

WORKDIR /project/sawtooth_healthcare

#COPY sawbuck_app/package.json /project/sawtooth-marketplace/sawbuck_app/

#RUN cd sawbuck_app/ && npm install

ENV PATH $PATH:/project/sawtooth_healthcare/bin
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
#CMD echo "\033[0;32m--- 2Building healthcare-rest-api ---\n\033[0m" \
#    && init-healthcare-rest-api.sh \
#    && healthcare-tp -v -C tcp://validator:4004