#!/bin/bash

supervisord -c /etc/supervisor/supervisord.conf &

 while :; do sleep 1; done
