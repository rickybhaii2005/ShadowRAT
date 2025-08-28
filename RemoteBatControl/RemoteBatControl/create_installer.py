#!/usr/bin/env python3
"""
RemoteBatControl Installer Creator

This script creates a standalone executable installer for the RemoteBatControl application.
It packages all necessary files and dependencies into a single executable file.
"""

import os
import sys
import subprocess
import shutil
import tempfile
import argparse
import platform
import zipfile
from pathlib import Path

def print_colored(message, color):
    """Print a colored message to the terminal"""
    colors = {
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'RED': '\033[91m',
        'RESET': '\033[0m',
        'BOLD': '\033[1m'
    }
    print(f"{colors[color]}{message}{colors['RESET']}")

def check_dependencies():
    """Check and install required dependencies"""
    print_colored("Checking dependencies...", "BOLD")
    
    # Check if PyInstaller is installed
    try:
        subprocess.check_call([sys.executable, "-m", "PyInstaller", "--version"], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
        print_colored("PyInstaller is already installed", "GREEN")
    except (subprocess.SubprocessError, FileNotFoundError):
        print_colored("Installing PyInstaller...", "YELLOW")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print_colored("PyInstaller installed successfully", "GREEN")
        except subprocess.CalledProcessError as e:
            print_colored(f"Failed to install PyInstaller: {e}", "RED")
            print_colored("Please install PyInstaller manually: pip install pyinstaller", "YELLOW")
            return False
    
    # Install required packages individually to avoid failing on one package
    print_colored("Installing required packages...", "BOLD")
    required_packages = [
        "flask",
        "flask-sqlalchemy",
        "gunicorn",
        "pillow",
        "psutil",
        "qrcode",
        "werkzeug",
        "pyinstaller",
        "pywin32"
    ]
    
    for package in required_packages:
        try:
            print_colored(f"Installing {package}...", "YELLOW")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                stdout=subprocess.DEVNULL, 
                                stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print_colored(f"Failed to install {package}, but continuing...", "YELLOW")
    
    print_colored("Dependencies installation completed", "GREEN")
    return True

def create_installer_script(temp_dir):
    """Create the installer script in the temporary directory"""
    installer_script = os.path.join(temp_dir, "installer.py")
    
    # Also save a copy to the current directory for debugging
    debug_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug_installer.py")
    
    script_content = '''
#!/usr/bin/env python3
"""
RemoteBatControl Installer
"""

import os
import sys
import shutil
import zipfile
import tempfile

# Embedded application data will be appended here during packaging
APP_DATA = b""

def install():
    print("Installing RemoteBatControl...")
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Extract files
        zip_path = os.path.join(temp_dir, "app.zip")
        
        # Get the path to the bundled app_data.bin file
        app_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_data.bin")
        
        if os.path.exists(app_data_path):
            # Copy the app_data.bin file to the zip_path
            shutil.copy2(app_data_path, zip_path)
        else:
            # Fallback to embedded APP_DATA if available
            if APP_DATA:
                with open(zip_path, "wb") as f:
                    f.write(APP_DATA)
            else:
                raise Exception("No application data found in installer")
        
        # Verify the zip file is valid
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                # Test the integrity of the zip file
                if zip_ref.testzip() is not None:
                    raise Exception("Zip file is corrupted")
                zip_ref.extractall(temp_dir)
        except zipfile.BadZipFile:
            raise Exception("Invalid zip file format")
        
        # Create installation directory in a location that doesn't require admin privileges
        # Use AppData/Local instead of Program Files
        install_dir = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~\AppData\Local")), "RemoteBatControl")
        os.makedirs(install_dir, exist_ok=True)
        
        # Copy files
        app_dir = os.path.join(temp_dir, "app")
        for item in os.listdir(app_dir):
            src = os.path.join(app_dir, item)
            dst = os.path.join(install_dir, item)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        
        print("Installation completed successfully!")
        print(f"RemoteBatControl has been installed to: {install_dir}")
        print("To start the application:")
        print("1. Navigate to the installation directory")
        print("2. Run RemoteBatControl.exe")
        print("3. Access the web interface at http://localhost:5000")
        print("4. Login with the default credentials:")
        print("   Username: subhashbswkrm")
        print("   Password: Sb13579@@@")
    except Exception as e:
        print(f"Error during installation: {e}")
    finally:
        shutil.rmtree(temp_dir)

def main():
    print("===== RemoteBatControl Installer =====")
    print("This will install RemoteBatControl on your system.")
    if input("Continue with installation? (y/n): ").lower() != 'y':
        print("Installation cancelled.")
        return
    
    install()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
'''
    
    with open(installer_script, "w") as f:
        f.write(script_content)
    
    # Write to debug file
    with open(debug_script, "w") as f:
        f.write(script_content)
    
    return installer_script

def create_spec_file(temp_dir, app_dir, console, icon):
    """Create a spec file for PyInstaller"""
    spec_file = os.path.join(temp_dir, "app.spec")
    
    # Format the icon parameter for the spec file
    icon_param = f"icon=r'{icon}'" if icon else "icon=None"
    
# Use the correct absolute path for server/server.py
    server_py_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../server/server.py')).replace('\\', '/')
    server_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../server')).replace('\\', '/')
    spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{server_py_path}'],
    pathex=['{server_dir_path}'],
    binaries=[],
    datas=[
        ('{os.path.join(app_dir, "templates").replace("\\", "/")}', 'templates'),
        ('{os.path.join(app_dir, "static").replace("\\", "/")}', 'static'),
        ('{os.path.join(app_dir, "uploads").replace("\\", "/")}', 'uploads'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='RemoteBatControl',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={console},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    {icon_param},
)
'''
    
    with open(spec_file, "w") as f:
        f.write(spec_content)
    
    return spec_file

def create_installer(output_name="RemoteBatControl_Installer", console=False, icon=None):
    """Create an installer executable for the application"""
    print_colored(f"Creating {output_name} installer...", "BOLD")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.join(current_dir, "RemoteBatControl")
    
    # Create a temporary directory for building
    temp_dir = tempfile.mkdtemp()
    try:
        # Create installer script
        installer_script = create_installer_script(temp_dir)
        
        # Create a temporary zip file containing the application
        app_zip = os.path.join(temp_dir, "app.zip")
        with zipfile.ZipFile(app_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Create app directory in the zip
            app_dir_in_zip = "app"
            
            # First, package the application using PyInstaller
            print_colored("Packaging application with PyInstaller...", "BOLD")
            
            # Create a spec file for PyInstaller
            spec_file = create_spec_file(temp_dir, app_dir, console, icon)
            
            # Run PyInstaller with the spec file
            subprocess.check_call([sys.executable, "-m", "PyInstaller", spec_file, "--distpath", os.path.join(temp_dir, "dist")])
            
            # Add the packaged application to the zip file
            app_dist_dir = os.path.join(temp_dir, "dist")
            for root, dirs, files in os.walk(app_dist_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.join(app_dir_in_zip, os.path.relpath(file_path, app_dist_dir)))
            
            # Add README and other documentation
            readme_content = """
# RemoteBatControl

RemoteBatControl is a remote administration tool that provides system monitoring and remote control capabilities.

## Features

- System monitoring (CPU, memory, disk usage)
- Process management
- Network monitoring
- Remote command execution
- File management
- Client management

## Installation

Run the installer and follow the on-screen instructions.

## Usage

1. Start RemoteBatControl from the desktop shortcut
2. Access the web interface at http://localhost:5000
3. Login with the default credentials:
   - Username: subhashbswkrm
   - Password: Sb13579@@@

## Security Warning

This tool provides administrative access to your system. Only use on trusted networks with strong authentication.
            """
            readme_path = os.path.join(temp_dir, "README.md")
            with open(readme_path, "w") as f:
                f.write(readme_content)
            zipf.write(readme_path, os.path.join(app_dir_in_zip, "README.md"))
        
        # Append the zip file to the installer script
        # Instead of embedding the zip data in the script, we'll use a separate file
        # that will be bundled with the installer
        app_data_path = os.path.join(temp_dir, "app_data.bin")
        
        # Copy the zip file to the app_data.bin file
        shutil.copy2(app_zip, app_data_path)
        
        # Modify the installer script to load the data from the bundled file
        with open(installer_script, "a") as f:
            f.write("\n# Embedded application data will be loaded from app_data.bin\nAPP_DATA = b\"\"  # Placeholder")
        
        # Create the final installer executable
        print_colored("Creating final installer executable...", "BOLD")
        pyinstaller_cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--name", output_name,
            "--add-binary", f"{app_data_path};.",  # Add the app_data.bin file as a binary
        ]
        
        if not console:
            pyinstaller_cmd.append("--windowed")
            
        if icon:
            pyinstaller_cmd.extend(["--icon", icon])
        
        pyinstaller_cmd.append(installer_script)
        
        # Run PyInstaller to create the installer
        subprocess.check_call(pyinstaller_cmd, cwd=temp_dir)
        
        # Copy the installer to the current directory
        installer_exe = os.path.join(temp_dir, "dist", f"{output_name}.exe")
        output_path = os.path.join(current_dir, f"{output_name}.exe")
        shutil.copy2(installer_exe, output_path)
        
        print_colored(f"Installer created successfully: {output_path}", "GREEN")
        return True
    except Exception as e:
        print_colored(f"Error creating installer: {e}", "RED")
        return False
    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Create an installer for RemoteBatControl")
    parser.add_argument("--name", default="RemoteBatControl_Installer", help="Name of the output installer")
    parser.add_argument("--console", action="store_true", help="Show console window when running the installer")
    parser.add_argument("--icon", help="Path to an icon file (.ico) for the installer")
    parser.add_argument("--skip-deps", action="store_true", help="Skip dependency installation")
    args = parser.parse_args()
    
    # Check and install dependencies
    if not args.skip_deps:
        if not check_dependencies():
            print_colored("Failed to install some dependencies. You can try running with --skip-deps to bypass dependency checks.", "RED")
            return 1
    else:
        print_colored("Skipping dependency installation...", "YELLOW")
    
    # Create the installer
    success = create_installer(
        output_name=args.name,
        console=args.console,
        icon=args.icon
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())