import scapy.all as scapy 
import socket
import sqlite3
from database import save_device
from flask import Flask , render_template, request,redirect ,url_for
from scapy.all import conf

app = Flask(__name__)




my_ip = socket.gethostbyname(socket.getfqdn())

#print(my_ip)

def get_ip():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

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

        hostname = get_hostname(ip)
        vendor = conf.manufdb._resolve_MAC(mac)

        devices.append({
            "ip": ip,
            "mac": mac,
            "hostname": hostname,
            "status": "Online",
            "vendor": vendor
        })
        status= "Online"
        save_device(ip, mac, hostname, "Online", vendor)

    return devices

#scanner(ip)

@app.route("/")
def home():
    return render_template("base.html", devices=[])


@app.route("/scan")
def scan():

    devices = scanner(ip)
    return render_template("index.html", devices=devices)


app.run(debug=True)

