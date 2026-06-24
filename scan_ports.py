import socket

ports_to_scan = [
    22,    # SSH
    53,    # DNS
    80,    # HTTP
    161,   # SNMP
    443,   # HTTPS
    445,   # SMB
    554,   # RTSP
    3389   # RDP
]

def scan_port(ip):
    open_ports = []

    for port in ports_to_scan:
        
        s=socket.socket(socket.AF_INET ,socket.SOCK_STREAM) 
        s.settimeout(0.5)

        if s.connect_ex((ip,port)) == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unkhown"
            open_ports.append(f"{port} {service} ")
        s.close()
    
    return open_ports


