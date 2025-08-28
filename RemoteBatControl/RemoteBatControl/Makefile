# Makefile for RemoteBatControl

.PHONY: setup run clean test lint package install uninstall help

# Default target
help:
	@echo "RemoteBatControl Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make setup     - Install dependencies"
	@echo "  make run       - Run the application"
	@echo "  make clean     - Remove build artifacts"
	@echo "  make test      - Run tests"
	@echo "  make lint      - Run linting"
	@echo "  make package   - Create executable package"
	@echo "  make install   - Install the application"
	@echo "  make uninstall - Uninstall the application"

# Install dependencies
setup:
	pip install -r requirements.txt

# Run the application
run:
	python RemoteBatControl/main.py

# Clean build artifacts
clean:
	rm -rf build dist *.egg-info __pycache__ RemoteBatControl/__pycache__
	python -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]"
	python -c "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__') if p.is_dir()]"

# Run tests
test:
	python -m unittest discover -s tests

# Run linting
lint:
	flake8 RemoteBatControl

# Create executable package
package:
	cd RemoteBatControl && python setup.py

# Install the application
install:
	cd RemoteBatControl && install.bat

# Uninstall the application
uninstall:
	cd RemoteBatControl && uninstall.bat