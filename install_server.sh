#!/bin/bash
# Installer script for ShadowRAT server

set -e

# Install Python dependencies
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Start the server
python3 RemoteBatControl/RemoteBatControl/RemoteBatControl/app.py
