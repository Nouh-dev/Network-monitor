import scapy.all as scapy
from scapy.all import conf
from .scan_ports import scan_port
from .network_topology import network_topologyy
from outils.get_hostname import get_hostname
from .detecter_os import detecter_os
from .detecter_devices import detecter_devices 
from database import save_device
from outils.device_exists import device_exists
from outils.get_device_from_db import get_device_from_db



devices =[]
def scanner(network):

    result = scapy.arping(network)[0]
    net = network_topologyy()
    global devices
    devices.clear()

    network_name = ".".join(network.split(".")[:3])
    
    for sent,received in result:

        ip = received.psrc
        mac = received.hwsrc

        hostname = get_hostname(ip)
        vendor = conf.manufdb._resolve_MAC(mac)
        
        if device_exists(ip):
            db_data = get_device_from_db(ip) 

            os_name = db_data["os_name"]
            ports_str = db_data["ports"]
            status_port = db_data["status_port"]

            ports = ports_str
            detecter_devices(
                net,
                ip,
                db_data["hostname"],
                db_data["os_name"],
                db_data["vendor"],
                db_data["ports"],
                mac
            )
        else:
            open_ports = scan_port(ip)
            ports_str = ", ".join(open_ports)
            status_port = "OPEN" if open_ports else "CLOSED"

            os_name = detecter_os(ip)

            save_device(
                ip, mac, hostname,
                "Online",
                os_name,
                vendor,
                ports_str,
                status_port,
                network_name
            )

            ports = " | ".join(open_ports)
            detecter_devices(net, ip, hostname, os_name, vendor, ports, mac)
    net.save_graph("templates/network.html")

    return devices