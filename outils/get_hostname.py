import socket

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return None