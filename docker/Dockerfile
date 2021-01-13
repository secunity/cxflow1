FROM    pmacct/nfacctd
# FROM    python:3.6

ADD     entrypoint.sh /

RUN     apt-get update && apt-get upgrade -y && apt-get autoremove -y &&\
        apt-get install -y python3-pip git &&\
        mkdir -p /etc/supervisor &&\
        mkdir -p /etc/secunity &&\
        git clone https://github.com/secunity/cxflow1.git /opt/secunity-cxflow &&\
        python3 -m pip install --upgrade pip setuptools &&\
        python3 -m pip install supervisor &&\
        python3 -m pip install -r /opt/secunity-cxflow/requirements.txt &&\
        chmod 777 /entrypoint.sh &&\
        chmod 777 /opt/secunity-cxflow/worker.py &&\
        chmod 777 /opt/secunity-cxflow/upgrader.py &&\
        chmod 777 /opt/secunity-cxflow/docker/entrypoint.py

ADD     supervisord.conf /etc/supervisor

ENV     PATH="/opt/secunity-cxflow:${PATH}"
ENV     PYTHONPATH=/opt/secunity-cxflow

WORKDIR /opt/secunity-cxflow

ENTRYPOINT /opt/secunity-cxflow/docker/entrypoint.py
# ENTRYPOINT /entrypoint.sh

# CMD ["/entrypoint.sh"]

#  rm -rf /opt/routers-stats-fetcher
