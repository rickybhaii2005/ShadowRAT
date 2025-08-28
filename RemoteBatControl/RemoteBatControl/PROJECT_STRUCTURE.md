# RemoteBatControl Project Structure

This document provides an overview of the RemoteBatControl project structure to help you understand how the codebase is organized.

## Directory Structure

```
RemoteBatControl/
├── RemoteBatControl/           # Main application directory
│   ├── app.py                  # Flask application initialization
│   ├── main.py                 # Application entry point
│   ├── client_handler.py       # Client management functionality
│   ├── network_scanner.py      # Network scanning functionality
│   ├── system_monitor.py       # System monitoring functionality
│   ├── stealth_keylogger.py    # Keylogger implementation
│   ├── deploy_keylogger.py     # Keylogger deployment utility
│   ├── qr_generator.py         # QR code generation utility
│   ├── setup.py                # PyInstaller packaging script
│   ├── verify_files.py         # File verification utility
│   ├── app_icon.svg            # Application icon
│   ├── setup_autostart.bat     # Windows autostart configuration
│   ├── start_monitor.bat       # Application startup script
│   ├── package_app.bat         # Packaging utility script
│   ├── install.bat             # Installation script
│   ├── static/                 # Static assets
│   │   ├── css/                # CSS stylesheets
│   │   └── js/                 # JavaScript files
│   ├── templates/              # HTML templates
│   │   ├── base.html           # Base template
│   │   ├── login.html          # Login page
│   │   ├── dashboard.html      # Main dashboard
│   │   ├── processes.html      # Process management
│   │   ├── network.html        # Network monitoring
│   │   ├── network_devices.html # Network devices
│   │   ├── remote_control.html # Remote control
│   │   ├── advanced_control.html # Advanced control
│   │   ├── file_manager.html   # File management
│   │   ├── client_manager.html # Client management
│   │   └── logs.html           # Log viewer
│   ├── uploads/                # File upload directory
│   │   └── .gitkeep            # Placeholder to track empty directory
│   ├── requirements.txt        # Python dependencies
│   ├── pyproject.toml          # Project metadata
│   ├── README.md               # Project documentation
│   ├── SOFTWARE_README.md      # Software packaging documentation
│   ├── KEYLOGGER_README.md     # Keylogger documentation
│   └── LICENSE                 # License file
├── .gitignore                  # Git ignore file
├── requirements.txt            # Root-level dependencies
├── LICENSE                     # Project license
├── README.md                   # Project overview
├── CHANGELOG.md                # Version history
├── RELEASE_NOTES.md            # Release information
├── CONTRIBUTING.md             # Contribution guidelines
├── CODE_OF_CONDUCT.md          # Community guidelines
├── SECURITY.md                 # Security policy
├── PROJECT_STRUCTURE.md        # This file
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
├── .dockerignore               # Docker ignore file
├── Makefile                    # Build automation
├── run.bat                     # Windows run script
├── run.sh                      # Unix run script
├── check_updates.py            # Update checker
├── check_updates.bat           # Windows update checker
├── check_updates.sh            # Unix update checker
├── generate_config.py          # Configuration generator
├── generate_config.bat         # Windows configuration generator
├── generate_config.sh          # Unix configuration generator
├── check_requirements.py       # Requirements checker
├── check_requirements.bat      # Windows requirements checker
├── check_requirements.sh       # Unix requirements checker
└── test_app.py                 # Application test script
```

## Core Components

### Application Core

- **app.py**: Initializes the Flask application, configures routes, and sets up middleware.
- **main.py**: Entry point for the application, runs the Flask server.
- **system_monitor.py**: Provides system monitoring functionality (CPU, memory, disk, processes).
- **client_handler.py**: Manages client connections and interactions.
- **network_scanner.py**: Implements network scanning and device discovery.

### Security Components

- **stealth_keylogger.py**: Implements keylogging functionality for monitoring keystrokes.
- **deploy_keylogger.py**: Utility for deploying the keylogger to target systems.

### Web Interface

- **templates/**: Contains HTML templates for the web interface.
- **static/**: Contains CSS, JavaScript, and other static assets.

### Utilities

- **setup.py**: Script for packaging the application into an executable.
- **verify_files.py**: Utility for verifying the presence of required files.
- **qr_generator.py**: Utility for generating QR codes for easy connection.

### Configuration and Deployment

- **package_app.bat**: Script for packaging the application.
- **install.bat**: Script for installing the application.
- **setup_autostart.bat**: Script for configuring autostart on Windows.
- **start_monitor.bat**: Script for starting the application.

### Documentation

- **README.md**: Main project documentation.
- **SOFTWARE_README.md**: Documentation for software packaging.
- **KEYLOGGER_README.md**: Documentation for the keylogger component.
- **CONTRIBUTING.md**: Guidelines for contributing to the project.
- **CODE_OF_CONDUCT.md**: Community guidelines.
- **SECURITY.md**: Security policy and vulnerability reporting.
- **CHANGELOG.md**: Version history and changes.
- **RELEASE_NOTES.md**: Release information and features.

## Development Workflow

1. **Setup**: Install dependencies using `pip install -r requirements.txt`.
2. **Run**: Start the application using `python RemoteBatControl/main.py`.
3. **Test**: Test the application using `python test_app.py`.
4. **Package**: Create an executable using `cd RemoteBatControl && python setup.py`.
5. **Install**: Install the application using `cd RemoteBatControl && install.bat`.

## Deployment Options

1. **Local Installation**: Install and run the application locally.
2. **Packaged Executable**: Create a standalone executable for distribution.
3. **Docker Container**: Deploy using Docker and Docker Compose.
4. **Web Deployment**: Deploy to a web hosting service like Netlify.

## Configuration

Use `generate_config.py` to create a custom configuration file for the application.

## Maintenance

- Check for updates using `check_updates.py`.
- Verify system requirements using `check_requirements.py`.