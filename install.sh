#!/bin/bash

if command -v python3 &>/dev/null; then
    echo "Python 3 is installed."
    python3 --version
else
    echo "Python 3 is not installed. Please install it and try again."
    exit 1
fi

if command -v pip3 &>/dev/null; then
    echo "pip3 is installed."
    pip3 --version
else
    echo "pip3 is not available. Please install pip for Python 3 and try again."
    exit 1
fi

pip3 install -r requirements.txt

chmod +x web_crawler.py

cp web_crawler.py /usr/local/bin/web_crawler

echo "Installation completed. You can now call your script with 'web_crawler'"
