
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
