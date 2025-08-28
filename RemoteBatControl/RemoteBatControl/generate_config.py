#!/usr/bin/env python3
"""
Configuration Generator for RemoteBatControl

This script generates a configuration file for the RemoteBatControl application.
It prompts the user for various settings and creates a config.json file.
"""

import os
import sys
import json
import getpass
import secrets
import string
from pathlib import Path

# Default configuration
DEFAULT_CONFIG = {
    "server": {
        "host": "0.0.0.0",
        "port": 5000,
        "debug": False
    },
    "authentication": {
        "username": "admin",
        "password": "StrongPassword123!",
        "session_timeout": 30  # minutes
    },
    "security": {
        "secret_key": secrets.token_hex(16),
        "max_login_attempts": 5,
        "lockout_time": 15  # minutes
    },
    "features": {
        "enable_keylogger": False,
        "enable_remote_command": True,
        "enable_file_management": True,
        "enable_power_control": True
    },
    "network_scanner": {
        "scan_timeout": 2,  # seconds
        "scan_threads": 10
    },
    "logging": {
        "level": "INFO",
        "file": "app.log"
    }
}

def generate_secret_key():
    """Generate a random secret key"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(24))

def prompt_user_for_config():
    """Prompt the user for configuration settings"""
    config = DEFAULT_CONFIG.copy()
    
    print("\nRemoteBatControl Configuration Generator")
    print("-" * 40)
    
    # Server settings
    print("\nServer Settings:")
    config["server"]["host"] = input(f"Host [0.0.0.0]: ") or "0.0.0.0"
    
    port_input = input(f"Port [5000]: ") or "5000"
    try:
        config["server"]["port"] = int(port_input)
    except ValueError:
        print("Invalid port number. Using default: 5000")
        config["server"]["port"] = 5000
    
    debug_input = input(f"Debug mode (True/False) [False]: ").lower() or "false"
    config["server"]["debug"] = debug_input == "true"
    
    # Authentication settings
    print("\nAuthentication Settings:")
    config["authentication"]["username"] = input(f"Username [admin]: ") or "admin"
    
    password = getpass.getpass(f"Password [leave empty for default]: ")
    if password:
        config["authentication"]["password"] = password
    
    # Security settings
    print("\nSecurity Settings:")
    config["security"]["secret_key"] = generate_secret_key()
    print(f"Generated secret key: {config['security']['secret_key']}")
    
    # Feature settings
    print("\nFeature Settings:")
    
    keylogger_input = input(f"Enable keylogger (True/False) [False]: ").lower() or "false"
    config["features"]["enable_keylogger"] = keylogger_input == "true"
    
    remote_command_input = input(f"Enable remote command execution (True/False) [True]: ").lower() or "true"
    config["features"]["enable_remote_command"] = remote_command_input == "true"
    
    file_management_input = input(f"Enable file management (True/False) [True]: ").lower() or "true"
    config["features"]["enable_file_management"] = file_management_input == "true"
    
    power_control_input = input(f"Enable power control (True/False) [True]: ").lower() or "true"
    config["features"]["enable_power_control"] = power_control_input == "true"
    
    return config

def save_config(config, config_path):
    """Save the configuration to a file"""
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"\nConfiguration saved to {config_path}")
        return True
    except Exception as e:
        print(f"\nError saving configuration: {str(e)}")
        return False

def main():
    """Main function"""
    # Determine the configuration file path
    config_dir = Path("RemoteBatControl")
    config_path = config_dir / "config.json"
    
    # Check if the configuration file already exists
    if config_path.exists():
        overwrite = input(f"\nConfiguration file already exists at {config_path}. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("Configuration generation cancelled.")
            return
    
    # Prompt the user for configuration settings
    config = prompt_user_for_config()
    
    # Save the configuration
    if save_config(config, config_path):
        print("\nConfiguration generation complete!")
        print("You can now start the application with the new configuration.")
    else:
        print("\nConfiguration generation failed.")

if __name__ == "__main__":
    main()