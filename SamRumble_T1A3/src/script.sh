#!/bin/bash
# check if python is installed
if command -v python3 &>/dev/null; then
    echo "Python is already installed"
else
    apt-get update
    apt-get install -y python3 #-y will select yes without any input
fi

# locate venv
venv_dir=".venv"

# check to see if a venv already exists
if [ -d "$venv_dir" ]; then
    source .venv/bin/activate
else
    python3 -m venv .venv
    echo "Time to launch venv!"
    source .venv/bin/activate
fi

# check is pip is installe 
if command -v pip3 &>/dev/null; then
    echo "pip is already installed"

else
    curl -O https://bootstrap.pypa.io/get-pip.py
fi

pip install -r requirements.txt

#remove clutter from terminal
clear

python3 main.py