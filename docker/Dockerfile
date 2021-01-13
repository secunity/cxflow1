FROM    pmacct/nfacctd
# FROM    python:3.6

ADD     entrypoint.sh /

RUN     apt-get update && apt-get upgrade -y && apt-get autoremove -y &&\
        apt-get install -y python3-pip git &&\
        mkdir -p /etc/supervisor &&\
        mkdir -p /etc/secunity &&\
        git clone https://github.com/secunity/cxflow1.git /opt/secunity-cxflow1 &&\
        python3 -m pip install --upgrade pip setuptools &&\
        python3 -m pip install supervisor &&\
        python3 -m pip install -r /opt/secunity-cxflow1/requirements.txt &&\
        chmod 777 /entrypoint.sh &&\
        chmod 777 /opt/secunity-cxflow1/worker.py &&\
        chmod 777 /opt/secunity-cxflow1/upgrader.py

ADD     supervisord.conf /etc/supervisor

ENV     PATH="/opt/secunity-cxflow1:${PATH}"
ENV     PYTHONPATH=/opt/secunity-cxflow1

WORKDIR /opt/secunity-cxflow1

ENTRYPOINT /entrypoint.sh

# CMD ["/entrypoint.sh"]

#  rm -rf /opt/routers-stats-fetcher
