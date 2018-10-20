#!/bin/bash
pip3 install virtualenv
virtualenv venv
source ./venv/bin/activate
pip3 install -U Flask
pip3 install -U Dash
pip3 install -U tensorflow
pip3 install -U tensorflow-gpu
pip3 install -U numpy
deactivate
