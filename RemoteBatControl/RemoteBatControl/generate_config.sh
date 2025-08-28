#!/bin/bash

echo "Generating configuration for RemoteBatControl..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Run the configuration generator script
python3 generate_config.py

echo "Press Enter to continue..."
read