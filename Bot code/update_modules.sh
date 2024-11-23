#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install/upgrade the modules listed in requirements.txt
pip install --upgrade -r requirements.txt

# Deactivate the virtual environment
deactivate
