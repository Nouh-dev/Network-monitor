import scapy.all as scapy # scan
import socket # ip/mac
import sqlite3
from database import save_device
from flask import Flask , render_template
from scapy.all import conf
from scan_ports import scan_port
import nmap # port/os
from pyvis.network import Network


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

#fonction principale
devices =[]
def scanner(network):

    result = scapy.arping(network)[0]
    global devices
    devices.clear()

    net = Network( height="700px",
                   width="100%",
                   bgcolor="white")

    net.add_node("internet",
                  label=" Internet", 
                  color="gray",
                  shape="image",
                  image = "static/icons/internet.png",
                  x=0, y = -800,
                  physics = False)

    net.add_node("router",
                 label=" Router",
                 color="gray",
                 size=30,
                 shape="image",
                 image = "static/icons/router.png",
                 x=0, y = -100,
                 physics = False) 
    
    net.add_node("grandstream",
                 label="Grandstream",
                 color="gray",
                 size=60,
                 shape="image",
                 image = "static/icons/grandstream.png",
                 x=0, y = 150,
                 physics = False) 
    
    net.add_node("firewall",
                 label=" Firewall",
                 color="red",
                 size=30,
                 shape="image",
                 x=0, y = -600,
                 image = "static/icons/firewall.png",
                 physics = False) 

    net.add_node("switch1",
                 label=" Switch 1",
                 color="blue",
                 shape="image",
                 image = "static/icons/switch.png",
                 x=0, y = -350,
                 physics = False) 
    
    net.add_node("switch2", 
                 label=" Switch 2", 
                 color="blue",
                 shape="image",
                 image = "static/icons/switch.png",
                 x=0, y = 400,
                 physics = False) 
    
    net.add_node("switch3", 
                 label=" Switch 3", 
                 color="blue",
                 shape="image",
                 image = "static/icons/switch.png",
                 x=0, y = 850,
                 physics = False) 
    
    net.add_edge("internet", "firewall") 
    net.add_edge("firewall", "switch1") 
    net.add_edge("switch1", "router") 
    net.add_edge("router", "grandstream") 
    net.add_edge("grandstream", "switch2")
    net.add_edge("switch2", "switch3")

    for sent, received in result:

        ip = received.psrc
        mac = received.hwsrc
        hostname = get_hostname(ip)
        vendor = conf.manufdb._resolve_MAC(mac)
        
        open_ports = scan_port(ip)
        status_port = "OPEN" if open_ports else "CLOSED"
        ports = " | ".join(open_ports)

        # Detecter OS 
        if (
        "445" in ports
        ):
            os_name = detecter_os(ip)
        else:
            os_name = "Unknown"
        
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
        detecter_devices(net,ip,hostname,os_name,vendor,ports,mac)
        ports_str = ", ".join(open_ports)
        save_device(ip, mac, hostname, "Online",os_name,vendor,ports_str,status_port)

    net.save_graph("templates/network.html")
    print(len(devices))

    return devices


#detercer os_name 

def detecter_os(target):
    scanner = nmap.PortScanner(
        nmap_search_path=(
            r"C:\Program Files (x86)\Nmap\nmap.exe",
        )
    )

    scanner.scan(target, arguments="-O -T5 --host-timeout 2s ")

    for host in scanner.all_hosts():

        os_matches = scanner[host].get("osmatch", [])

        if len(os_matches) > 0:

            best_os = os_matches[0]

            return best_os["name"]

    return "Unknown"


# Cartographie 

# ==========================
# Positions des switches
# ==========================

switch_pos = {
    "switch1": (-400, -350),
    "switch2": (0, 400),
    "switch3": (0, 650)
}

# Nombre de devices par switch
device_count = {
    "switch1": 0,
    "switch2": 0,
    "switch3": 0
}


def get_position(switch):

    sx, sy = switch_pos[switch]

    i = device_count[switch]
    device_count[switch] += 1

    cols = 20

    row = i // cols
    col = i % cols

    spacing_x = 120
    spacing_y = 100

    x = sx + (col - (cols - 1) / 2) * spacing_x
    y = sy + 120 + row * spacing_y

    return x, y
#detecter devices

def detecter_devices(net, ip, hostname, os_name, vendor, ports, mac):


    hostname = (hostname or "").upper()
    os_name = (os_name or "").upper()
    vendor = (vendor or "").upper()
    ports = " ".join(ports).upper()

    title = f""" 
    IP : {ip} 
    MAC : {mac}
    Hostname : {hostname}
    Vendor : {vendor}
    OS : {os_name}
    Ports : {ports} """ 

    node = ip

    # SERVER 
    if ("SERVER" in os_name 
        or "MSL-SRV" in hostname 
        or "REP-CASSRV" in hostname 
        or "MSL-CASSRV" in hostname 
        or "LDI-SRV" in hostname 
        or "BACKUP" in hostname):
        x, y = get_position("switch2") 
        net.add_node(node,
                     label=hostname,
                     title=title,
                     color="purple",
                     shape="image",
                     x=x,y=y,
                     image="static/icons/server.png",
                     physics=False) 
        net.add_edge("switch2",node) 

    # CAMERA 
    elif   ("554" in ports
    or "8554" in ports
    or "HIKVISION" in vendor
    or "CAMERA" in hostname
   ):
        x, y = get_position("switch1")
        net.add_node(node,
                     label=" Camera",
                     title=title,
                     color="pink",
                     size=20,
                     shape="image",
                     image="static/icons/camera.png",
                     x=x,y=y,
                     physics=False) 
        net.add_edge("switch1",node) 

    # NAS 
    elif ("QNAP" in vendor 
          or "ASUSTEK" in vendor 
          or "NAS" in hostname): 
        x, y = get_position("switch3")
        net.add_node(node,
                     label=" NAS",
                     title=title,
                     color="brown",
                     size=20,
                     shape="image",
                     image="static/icons/nas.png",
                     x=x,y=y,
                     physics=False) 
        net.add_edge("switch3",node) 

    # PRINTER 
    elif ("RICOH" in vendor 
          or "HP" in vendor 
          or "CANON" in vendor 
          or "BROTHER" in vendor 
          or "EPSON" in vendor): 
          x, y = get_position("switch3")
          net.add_node(node,
                       label=" Printer",
                       title=title,
                       color="yellow",
                       size=20,
                       shape="image",
                       image="static/icons/printer.png",
                       x=x,y=y,
                       physics=False) 
          net.add_edge("switch3",node) 

    # ACCESS POINT
    elif ("OPENWRT" in os_name
          or "AP" in hostname): 
          x, y = get_position("switch3")
          net.add_node(node,
                       label=" Access Point",
                       title=title,
                       color="cyan",
                       size=20,
                       shape="image",
                       image="static/icons/access_point.png",
                       x=x,y=y,
                       physics=False) 
          net.add_edge("switch3",node) 

    # IP PHONE 
    elif ("5060" in ports or "5061" in ports):
        x, y = get_position("switch3") 
        net.add_node(node,
                     label=" IP Phone",
                     title=title,
                     color="green",
                     size=20,
                     shape="image",
                     image="static/icons/phone.png",
                     x=x,y=y,
                     physics=False) 
        net.add_edge("switch3",node) 

    # PC 
    elif ("WINDOWS" in os_name 
          or "DESKTOP" in hostname 
          or "PC" in hostname 
          or "LAPTOP" in hostname):
          x, y = get_position("switch3") 
          net.add_node(node,
                       label=hostname,
                       title=title,
                       color="lime",
                       size=20,
                       shape="image",
                       image="static/icons/pc.png",
                       x=x,y=y,
                       physics=False) 
          net.add_edge("switch3",node) 

    # UNKNOWN 
    else: 
        x, y = get_position("switch3")
        net.add_node(node,
                     label=ip,
                     title=title,
                     color="lightgray",
                     size=20,
                     shape="image",
                     image="static/icons/unkhown.png",
                     x=x,y=y,
                     physics=False) 
        net.add_edge("switch3",node)



#scanner(ip)

@app.route("/")
def home():
    return render_template("base.html", devices=[])


@app.route("/scan")
def scan():

    devices = scanner(ip)
    return render_template("index.html", devices=devices)

@app.route("/cartographie")
def schéma():
    return render_template("network.html")

app.run(debug=True)

