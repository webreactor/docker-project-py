FROM ubuntu:14.04

RUN apt-get update \
    && apt-get install -y git python-setuptools make libpython3.4-dev \
    && easy_install pip \
    && pip install virtualenv

