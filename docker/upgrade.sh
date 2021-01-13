#!/bin/bash

supervisorctl stop secunity-cxflow

cd /opt/secunity-cxflow && git fetch && git pull && find . -name '*.pyc' -delete

supervisorctl start secunity-cxflow
