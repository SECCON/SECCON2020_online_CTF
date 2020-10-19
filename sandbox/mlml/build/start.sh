#!/bin/sh
set -eu

cd /home/moratorium08/build
python3 proof-of-work.py &&\
python3 start_docker.py
