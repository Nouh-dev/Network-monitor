import socket


def get_ip():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # créer une IPv4 et UDP

    try:
        s.connect(("10.255.255.255",1))
        local_ip = s.getsockname()[0]
    except:
        local_ip = "127.0.0.1"
    finally:
        s.close()
    parts = local_ip.split(".")
    local_ip =f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"

    return local_ip