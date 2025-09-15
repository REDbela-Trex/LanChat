import socket
import threading
import json
from utils import encrypt, decrypt

BUFFER_SIZE = 1024
SERVER_KEY = "secret123"

def scan_lan_servers(update_server_list):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_sock.bind(("", 5051))
    servers = {}
    while True:
        try:
            data, addr = udp_sock.recvfrom(1024)
            info = json.loads(data.decode())
            ip = info["ip"]
            if ip not in servers:
                servers[ip] = f"{info['name']} ({info['port']})"
                update_server_list(servers)
        except:
            continue

def connect_to_server(ip, port, update_ui):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
    except Exception as e:
        update_ui(f"[CLIENT] Bağlanamadı: {e}")
        return None
    
    update_ui(f"[CLIENT] Bağlandı: {ip}:{port}")
    
    def receive_messages():
        while True:
            try:
                data = sock.recv(BUFFER_SIZE)
                if not data:
                    break
                text = decrypt(data, SERVER_KEY)
                update_ui(f"{ip}: {text}")
            except:
                break
        sock.close()
        update_ui(f"[CLIENT] Bağlantı kapandı: {ip}:{port}")
    
    threading.Thread(target=receive_messages, daemon=True).start()
    return sock

def send_message(sock, message):
    if sock:
        sock.send(encrypt(message, SERVER_KEY))
