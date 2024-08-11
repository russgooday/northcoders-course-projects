#!/bin/bash

# Define the virtual environment directory
VENV_DIR="venv"

# Script needs to be executed with source
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "${SECONDARY}Script needs to be executed with source e.g.$ ${PRIMARY}source ${BASH_SOURCE[0]}"
    exit 1
fi

# Check if the virtual environment directory exists
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python -m venv $VENV_DIR
else
  echo "Virtual environment already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Install dependencies
if [ -f "requirements.txt" ]; then
  echo "Installing dependencies..."
  pip install -r requirements.txt
else
  echo "requirements.txt not found, skipping dependency installation."
fi

# Optionally, set environment variables
echo "Setting environment variables..."
export PYTHONPATH=$(pwd)

# Notify the user
echo "Setup complete. Virtual environment is ready and activated."
echo "To deactivate the virtual environment, run 'deactivate'."