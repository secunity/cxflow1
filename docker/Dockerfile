FROM        pmacct/base
MAINTAINER  Secunity LTD. (support@secunity.io)

ENV         PATH="/opt/secunity-cxflow:${PATH}"
ENV         PYTHONPATH=/opt/secunity-cxflow

RUN         apt-get update && apt-get upgrade -y && apt-get autoremove -y &&\
            apt-get install -y python3-pip git &&\
            mkdir -p /etc/supervisor &&\
            mkdir -p /etc/secunity &&\
            git clone https://github.com/secunity/cxflow1.git /opt/secunity-cxflow &&\
            python3 -m pip install --upgrade pip setuptools &&\
            python3 -m pip install supervisor &&\
            python3 -m pip install -r /opt/secunity-cxflow/requirements.txt &&\
            cp /opt/secunity-cxflow/docker/entrypoint.sh / &&\
            chmod 777 /opt/secunity-cxflow/worker.py &&\
            chmod 777 /opt/secunity-cxflow/upgrader.py &&\
            chmod 777 /opt/secunity-cxflow/docker/entrypoint.py &&\
            chmod 777 /opt/secunity-cxflow/docker/entrypoint.sh &&\
            chmod 777 /opt/secunity-cxflow/docker/upgrade.sh &&\
            chmod 777 /entrypoint.sh

ADD         supervisord.conf /etc/supervisor

WORKDIR     /opt/secunity-cxflow

ENTRYPOINT  /entrypoint.sh
