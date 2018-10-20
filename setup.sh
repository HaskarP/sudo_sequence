#!/bin/bash
pip install virtualenv
virtualenv venv
source ./venv/bin/activate
pip install -U Flask
pip install -U Dash
