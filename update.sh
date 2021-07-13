#!/bin/bash

# update codebase from main
git checkout origin main
git fetch origin main
git pull

# activate venv
source venv/bin/activate

# install any additional requirements
pip3 install -r requirements.txt