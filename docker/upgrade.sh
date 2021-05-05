#!/bin/bash

supervisorctl stop $SECUNITYAPP

cd /opt/$SECUNITYAPP &&\
git fetch &&\
git pull &&\
git checkout $SECUNITYBRANCH &&\
git pull &&\
find /opt/$SECUNITYAPP -name '*.pyc' -delete

supervisorctl start $SECUNITYAPP
