import socket

def encrypt(message: str, key: str) -> bytes:
    return bytes([b ^ ord(key[i % len(key)]) for i, b in enumerate(message.encode())])

def decrypt(message: bytes, key: str) -> str:
    return "".join([chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(message)])

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip
