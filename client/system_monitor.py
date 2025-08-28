import psutil
import platform
import os
import subprocess
import logging
import socket
import ipaddress
import threading
import queue
from datetime import datetime, timedelta
from typing import Dict, List, Any

class SystemMonitor:
    """System monitoring utility class"""
    def __init__(self):
        self.safe_log_paths = [
            '/var/log/syslog',
            '/var/log/messages',
            '/var/log/kern.log',
            '/var/log/auth.log',
            'C:\\Windows\\System32\\winevt\\Logs\\System.evtx',
            'C:\\Windows\\System32\\winevt\\Logs\\Application.evtx'
        ]

    def get_system_info(self) -> Dict[str, Any]:
        """Get basic system information"""
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            return {
                'hostname': platform.node(),
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'boot_time': boot_time.strftime('%Y-%m-%d %H:%M:%S'),
                'uptime': str(uptime).split('.')[0],  # Remove microseconds
                'cpu_count': psutil.cpu_count(),
                'cpu_count_logical': psutil.cpu_count(logical=True)
            }
        except Exception as e:
            logging.error(f"Error getting system info: {e}")
            return {'error': str(e)}

    def get_system_stats(self) -> Dict[str, Any]:
        """Get real-time system statistics"""
        try:
            # ...existing code...
            pass
        except Exception as e:
            logging.error(f"Error getting system stats: {e}")
            return {'error': str(e)}
