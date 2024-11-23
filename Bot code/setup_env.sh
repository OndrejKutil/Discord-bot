#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

deactivate

echo "Virtual environment setup complete."

# Don't forget to add execute permissions to this script:
# chmod +x setup_env.sh