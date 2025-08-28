#!/bin/bash

echo "Checking for RemoteBatControl updates..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Run the update checker script
python3 check_updates.py

echo "Press Enter to continue..."
read