#!/usr/bin/env python3
"""
Test script for RemoteBatControl

This script performs basic tests to verify that the application is working correctly.
It checks for the presence of required files, tests the connection to the server,
and verifies that the authentication system is working.
"""

import os
import sys
import time
import requests
import subprocess
from pathlib import Path

# Colors for terminal output
COLORS = {
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m',
    'RESET': '\033[0m',
    'BOLD': '\033[1m'
}

def print_colored(message, color):
    """Print a colored message to the terminal"""
    print(f"{COLORS[color]}{message}{COLORS['RESET']}")

def check_files():
    """Check if all required files are present"""
    print_colored("Checking for required files...", "BOLD")
    
    required_files = [
        "RemoteBatControl/app.py",
        "RemoteBatControl/main.py",
        "RemoteBatControl/system_monitor.py",
        "RemoteBatControl/client_handler.py",
        "RemoteBatControl/network_scanner.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print_colored(f"Missing required files: {', '.join(missing_files)}", "RED")
        return False
    
    print_colored("All required files are present.", "GREEN")
    return True

def start_server():
    """Start the server in a separate process"""
    print_colored("Starting the server...", "BOLD")
    
    try:
        # Change directory to RemoteBatControl
        os.chdir("RemoteBatControl")
        
        # Start the server
        server_process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Give the server time to start
        time.sleep(3)
        
        # Check if the server is running
        if server_process.poll() is not None:
            stdout, stderr = server_process.communicate()
            print_colored(f"Server failed to start: {stderr.decode()}", "RED")
            return None
        
        print_colored("Server started successfully.", "GREEN")
        return server_process
    
    except Exception as e:
        print_colored(f"Error starting server: {str(e)}", "RED")
        return None
    
    finally:
        # Change back to the original directory
        os.chdir("..")

def test_connection(server_process):
    """Test the connection to the server"""
    print_colored("Testing connection to the server...", "BOLD")
    
    try:
        # Try to connect to the server
        response = requests.get("http://localhost:5000/")
        
        if response.status_code == 200:
            print_colored("Connection successful.", "GREEN")
            return True
        else:
            print_colored(f"Connection failed with status code: {response.status_code}", "RED")
            return False
    
    except requests.exceptions.ConnectionError:
        print_colored("Connection failed. Server is not responding.", "RED")
        return False
    
    except Exception as e:
        print_colored(f"Error testing connection: {str(e)}", "RED")
        return False

def test_authentication():
    """Test the authentication system"""
    print_colored("Testing authentication system...", "BOLD")
    
    try:
        # Try to login with default credentials
        response = requests.post(
            "http://localhost:5000/login",
            data={"username": "subhashbswkrm", "password": "Sb13579@@@"}
        )
        
        if response.status_code == 200 and "dashboard" in response.url:
            print_colored("Authentication successful.", "GREEN")
            return True
        else:
            print_colored("Authentication failed.", "RED")
            return False
    
    except Exception as e:
        print_colored(f"Error testing authentication: {str(e)}", "RED")
        return False

def main():
    """Main function"""
    print_colored("RemoteBatControl Test Script", "BOLD")
    print("-" * 30)
    
    # Check if all required files are present
    if not check_files():
        print_colored("Test failed: Missing required files.", "RED")
        return
    
    # Start the server
    server_process = start_server()
    if server_process is None:
        print_colored("Test failed: Could not start server.", "RED")
        return
    
    try:
        # Test the connection to the server
        if not test_connection(server_process):
            print_colored("Test failed: Could not connect to server.", "RED")
            return
        
        # Test the authentication system
        if not test_authentication():
            print_colored("Test failed: Authentication system not working.", "RED")
            return
        
        # All tests passed
        print_colored("All tests passed! The application is working correctly.", "GREEN")
    
    finally:
        # Stop the server
        if server_process is not None:
            print_colored("Stopping the server...", "BOLD")
            server_process.terminate()
            server_process.wait()
            print_colored("Server stopped.", "GREEN")

if __name__ == "__main__":
    main()