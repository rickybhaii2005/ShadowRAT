#!/usr/bin/env python3
"""
System Requirements Checker for RemoteBatControl

This script checks if the system meets the requirements for running the RemoteBatControl application.
It verifies Python version, required packages, and system capabilities.
"""

import os
import sys
import platform
import subprocess
import importlib.util

# Colors for terminal output
COLORS = {
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m',
    'BLUE': '\033[94m',
    'RESET': '\033[0m',
    'BOLD': '\033[1m'
}

# Minimum required Python version
MIN_PYTHON_VERSION = (3, 7)

# Required packages
REQUIRED_PACKAGES = [
    "flask",
    "psutil",
    "werkzeug",
    "flask_sqlalchemy",
    "email_validator",
    "pillow",
    "qrcode"
]

# Optional packages
OPTIONAL_PACKAGES = [
    "pyinstaller",
    "cairosvg"
]

def print_colored(message, color):
    """Print a colored message to the terminal"""
    print(f"{COLORS[color]}{message}{COLORS['RESET']}")

def check_python_version():
    """Check if the Python version meets the minimum requirement"""
    print_colored("Checking Python version...", "BOLD")
    
    current_version = sys.version_info[:2]
    version_str = f"{current_version[0]}.{current_version[1]}"
    
    if current_version >= MIN_PYTHON_VERSION:
        print_colored(f"Python version {version_str} - OK", "GREEN")
        return True
    else:
        min_version_str = f"{MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}"
        print_colored(f"Python version {version_str} is below the minimum required version {min_version_str}", "RED")
        return False

def check_package(package_name):
    """Check if a package is installed"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def check_required_packages():
    """Check if all required packages are installed"""
    print_colored("\nChecking required packages...", "BOLD")
    
    all_packages_installed = True
    missing_packages = []
    
    for package in REQUIRED_PACKAGES:
        if check_package(package):
            print_colored(f"{package} - OK", "GREEN")
        else:
            print_colored(f"{package} - Missing", "RED")
            missing_packages.append(package)
            all_packages_installed = False
    
    return all_packages_installed, missing_packages

def check_optional_packages():
    """Check if optional packages are installed"""
    print_colored("\nChecking optional packages...", "BOLD")
    
    for package in OPTIONAL_PACKAGES:
        if check_package(package):
            print_colored(f"{package} - OK", "GREEN")
        else:
            print_colored(f"{package} - Not installed (optional)", "YELLOW")

def check_system_capabilities():
    """Check system capabilities"""
    print_colored("\nChecking system capabilities...", "BOLD")
    
    # Check operating system
    os_name = platform.system()
    print_colored(f"Operating System: {os_name}", "BLUE")
    
    if os_name == "Windows":
        print_colored("Windows is fully supported - OK", "GREEN")
    elif os_name == "Linux":
        print_colored("Linux is supported, but some features may be limited - OK", "YELLOW")
    elif os_name == "Darwin":
        print_colored("macOS is supported, but some features may be limited - OK", "YELLOW")
    else:
        print_colored(f"Unknown operating system: {os_name} - Support may be limited", "RED")
    
    # Check for admin/root privileges
    is_admin = False
    if os_name == "Windows":
        try:
            # This will raise an exception if not admin
            is_admin = os.path.exists("C:\\Windows\\temp")
        except:
            is_admin = False
    else:
        is_admin = os.geteuid() == 0
    
    if is_admin:
        print_colored("Admin/root privileges - OK", "GREEN")
    else:
        print_colored("Admin/root privileges - Not available (some features may be limited)", "YELLOW")
    
    # Check available disk space
    try:
        if os_name == "Windows":
            disk = "C:\\"
        else:
            disk = "/"
        
        total, used, free = shutil.disk_usage(disk)
        free_gb = free / (1024 ** 3)
        
        if free_gb > 1.0:
            print_colored(f"Available disk space: {free_gb:.2f} GB - OK", "GREEN")
        else:
            print_colored(f"Available disk space: {free_gb:.2f} GB - Low (at least 1 GB recommended)", "YELLOW")
    except:
        print_colored("Could not determine available disk space", "YELLOW")

def install_missing_packages(missing_packages):
    """Offer to install missing packages"""
    if not missing_packages:
        return
    
    print_colored("\nWould you like to install the missing packages? (y/n): ", "BOLD"), 
    choice = input().lower()
    
    if choice == 'y':
        print_colored("\nInstalling missing packages...", "BOLD")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print_colored("\nPackages installed successfully!", "GREEN")
        except subprocess.CalledProcessError as e:
            print_colored(f"\nError installing packages: {str(e)}", "RED")
            print_colored("Please install the packages manually using pip:", "YELLOW")
            print_colored(f"pip install {' '.join(missing_packages)}", "YELLOW")

def main():
    """Main function"""
    print_colored("RemoteBatControl System Requirements Checker", "BOLD")
    print("-" * 45)
    
    # Check Python version
    python_ok = check_python_version()
    
    # Check required packages
    packages_ok, missing_packages = check_required_packages()
    
    # Check optional packages
    check_optional_packages()
    
    # Check system capabilities
    check_system_capabilities()
    
    # Summary
    print_colored("\nSummary:", "BOLD")
    
    if python_ok and packages_ok:
        print_colored("Your system meets all the requirements for running RemoteBatControl!", "GREEN")
    elif python_ok and not packages_ok:
        print_colored("Your system meets the Python version requirement, but some packages are missing.", "YELLOW")
        install_missing_packages(missing_packages)
    else:
        print_colored("Your system does not meet the requirements for running RemoteBatControl.", "RED")
        print_colored("Please update Python to version 3.7 or higher.", "YELLOW")

if __name__ == "__main__":
    # Import shutil here to avoid potential issues
    import shutil
    main()