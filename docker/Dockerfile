FROM        pmacct/base
MAINTAINER  Secunity LTD. (support@secunity.io)

ENV         SECUNITYAPP="secunity-cxflow"
ENV         PATH="/opt/$SECUNITYAPP:${PATH}"
ENV         PYTHONPATH=/opt/$SECUNITYAPP
ENV         SECUNITYBRANCH="noyaml"

ADD         image-builder.sh /opt

RUN         bash -x /opt/image-builder.sh && rm /opt/image-builder.sh
#RUN         apt-get update && apt-get upgrade -y && apt-get autoremove -y &&\
#            apt-get install -y python3-pip git &&\
#            mkdir -p /etc/supervisor &&\
#            python3 -m pip install --upgrade pip setuptools &&\
#            python3 -m pip install supervisor &&\
#            mkdir -p /etc/secunity &&\
#            git clone https://github.com/secunity/cxflow1.git /opt/$SECUNITYAPP &&\
#            cd /opt/$SECUNITYAPP &&\
#            git checkout $SECUNITYBRANCH &&\
#            python3 -m pip install -r /opt/$SECUNITYAPP/requirements.txt &&\
#            cp /opt/$SECUNITYAPP/docker/entrypoint.sh / &&\
#            chmod 777 /opt/$SECUNITYAPP/worker.py &&\
#            chmod 777 /opt/$SECUNITYAPP/docker/upgrade.sh &&\
#            chmod 777 /opt/$SECUNITYAPP/upgrader.py &&\
#            chmod 777 /entrypoint.sh

#  ADD         supervisord.conf /etc/supervisor

WORKDIR     /opt/$SECUNITYAPP

ENTRYPOINT  /entrypoint.sh
