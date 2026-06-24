import scapy.all as scapy 
import socket
import sqlite3
from database import save_device
from flask import Flask , render_template, request,redirect ,url_for
from scapy.all import conf
from scan_ports import scan_port
import nmap


app = Flask(__name__)



#print(my_ip)

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


ip=get_ip()

#print(ip)


def get_assets():
    conn = sqlite3.connect("network.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM assets")
    data = cursor.fetchall()
    conn.close()
    return data 


assets = get_assets()
#print(assets)


def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return None

devices =[]
def scanner(network):

    result = scapy.arping(network)[0]
    global devices
    devices.clear()

    for sent, received in result:

        ip = received.psrc
        mac = received.hwsrc
        os_name = detecter_os(ip)
        hostname = get_hostname(ip)
        vendor = conf.manufdb._resolve_MAC(mac)
        
        open_ports = scan_port(ip)
        status_port = "OPEN" if open_ports else "CLOSED"
        ports = " | ".join(open_ports)
        print(vendor,ports,status_port,"\n",os_name)
        print("__________________________________________________________________________________")

        devices.append({
            "ip": ip,
            "mac": mac,
            "hostname": hostname,
            "status": "Online",
            "os_name": os_name,
            "vendor": vendor,
            "ports": "<br>".join(open_ports),
            "status_port":status_port
        })
        ports_str = ", ".join(open_ports)
        save_device(ip, mac, hostname, "Online",os_name,vendor,ports_str,status_port)

    return devices

#detercer os_name 

def detecter_os(target):
    scanner = nmap.PortScanner(
        nmap_search_path=(
            r"C:\Program Files (x86)\Nmap\nmap.exe",
        )
    )

    scanner.scan(target, arguments="-O --host-timeout 10s ")

    for host in scanner.all_hosts():

        os_matches = scanner[host].get("osmatch", [])

        if len(os_matches) > 0:

            best_os = os_matches[0]

            return best_os["name"]

    return "Unknown"





#scanner(ip)

@app.route("/")
def home():
    return render_template("base.html", devices=[])


@app.route("/scan")
def scan():

    devices = scanner(ip)
    return render_template("index.html", devices=devices)


app.run(debug=True)

