#!/bin/bash
pip3 install virtualenv
virtualenv --system-site-packages -p python3 venv
source ./venv/bin/activate
pip3 install --upgrade pip
pip3 install -U Flask
pip3 install -U Dash
pip3 install -U tensorflow
pip3 install -U tensorflow-gpu
pip3 install -U numpy
deactivate
