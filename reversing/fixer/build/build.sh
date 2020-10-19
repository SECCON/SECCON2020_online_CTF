#!/bin/sh

python3.9 -m compileall fixer.py
cp __pycache__/fixer.cpython-39.pyc ../dist/
