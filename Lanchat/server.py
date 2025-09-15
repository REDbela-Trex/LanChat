import socket
import threading
import json
from utils import encrypt, decrypt, get_local_ip

TCP_PORT = 5050
UDP_PORT = 5051
BUFFER_SIZE = 1024
connected_clients = []

SERVER_KEY = "secret123"

def start_tcp_server(update_ui):
    global connected_clients
    connected_clients = []
    local_ip = get_local_ip()
    
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sock.bind((local_ip, TCP_PORT))
    tcp_sock.listen(5)
    
    update_ui(f"[SERVER] TCP başlatıldı: {local_ip}:{TCP_PORT}")
    
    def handle_client(conn, addr):
        update_ui(f"[SERVER] {addr} bağlandı.")
        while True:
            try:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                text = decrypt(data, SERVER_KEY)
                update_ui(f"{addr[0]}: {text}")
                for c in connected_clients:
                    if c != conn:
                        try:
                            c.send(data)
                        except:
                            pass
            except:
                break
        connected_clients.remove(conn)
        conn.close()
        update_ui(f"[SERVER] {addr} bağlantısı kesildi.")
    
    def accept_clients():
        while True:
            conn, addr = tcp_sock.accept()
            connected_clients.append(conn)
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    
    threading.Thread(target=accept_clients, daemon=True).start()

def start_udp_broadcast(server_name):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    local_ip = get_local_ip()
    while True:
        msg = json.dumps({"name": server_name, "ip": local_ip, "port": TCP_PORT})
        udp_sock.sendto(msg.encode(), ("<broadcast>", UDP_PORT))
        threading.Event().wait(2)  # 2 saniye bekle
