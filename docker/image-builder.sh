#!/bin/bash


apt-get update && apt-get upgrade -y && apt-get autoremove -y &&\
apt-get install -y python3-pip git

mkdir -p /etc/secunity && chmod +rw /etc/secunity

# python3 -m pip install --upgrade pip setuptools &&\
python3 -m pip install supervisor &&\

git clone https://github.com/secunity/cxflow1.git $PYTHONPATH &&\
cd $PYTHONPATH &&\
git checkout $SECUNITYBRANCH &&\
python3 -m pip install -r $PYTHONPATH/requirements.txt &&\
cp $PYTHONPATH/docker/entrypoint.sh / &&\
chmod 777 /opt/$SECUNITYAPP/worker.py &&\
chmod 777 /opt/$SECUNITYAPP/docker/upgrade.sh &&\
chmod 777 /opt/$SECUNITYAPP/upgrader.py &&\
chmod 777 /entrypoint.sh

mkdir -p /etc/supervisor && chmod +rw /etc/supervisor
rm /etc/supervisor/supervisord.conf

cat << 'EOF' >> /etc/supervisor/supervisord.conf

[unix_http_server]
file=/tmp/supervisor.sock   ; the path to the socket file

[supervisord]
logfile=/tmp/supervisord.log ; main log file; default $CWD/supervisord.log
logfile_maxbytes=50MB        ; max main logfile bytes b4 rotation; default 50MB
logfile_backups=10           ; # of main logfile backups; 0 means none, default 10
loglevel=info                ; log level; default info; others: debug,warn,trace
pidfile=/tmp/supervisord.pid ; supervisord pidfile; default supervisord.pid
nodaemon=false               ; start in foreground if true; default false
minfds=1024                  ; min. avail startup file descriptors; default 1024
minprocs=200                 ; min. avail process descriptors;default 200

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///tmp/supervisor.sock ; use a unix:// URL  for a unix socket

[program:nfacctd]
command=/usr/local/sbin/nfacctd -f /etc/secunity/nfacctd.conf
autostart=false

[program:sfacctd]
command=/usr/local/sbin/sfacctd -f /etc/secunity/sfacctd.conf
autostart=false

[program:secunity-cxflow]
command=python3 /opt/secunity-cxflow/worker.py
autostart=true
numprocs=1
# environment=PYTHONPATH=/opt/secunity-cxflow


# [program:secunity-upgrader]
# command=python3 /opt/routers-stats-fetcher/upgrader.py
# environment=PYTHONPATH=/opt/routers-stats-fetcher
# autostart=true
# numprocs=1

EOF

