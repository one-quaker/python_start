#!/bin/bash

# docker+docker-compose install script for ubuntu linux

# install
# sh -c "$(wget https://raw.githubusercontent.com/one-quaker/python_start/master/install_docker.sh -O -)"

FN='install_docker.py'
RUN_FP=/tmp/$FN

wget "https://raw.githubusercontent.com/one-quaker/python_start/master/$FN" -O $RUN_FP
python $RUN_FP
rm $RUN_FP
