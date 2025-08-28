import sys
import os
# Add RemoteBatControl/RemoteBatControl/RemoteBatControl to sys.path for app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../RemoteBatControl/RemoteBatControl/RemoteBatControl')))
# Add server and client to sys.path for handler and monitor modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../server')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../client')))
from RemoteBatControl.RemoteBatControl.RemoteBatControl.app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
