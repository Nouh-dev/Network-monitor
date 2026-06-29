from outils.server import Server
from outils.printer import vendor_printer

def detecter_devices(net, ip, hostname, os_name, vendor, ports, mac):
    
    hostname = (hostname or "").upper()
    os_name = (os_name or "").upper()
    vendor = (vendor or "").upper()
    ports = (ports or "").upper()

    title = f""" 
    IP : {ip} 
    MAC : {mac}
    Hostname : {hostname}
    Vendor : {vendor}
    OS : {os_name}
    Ports : {ports} """ 

    node = ip
    

    # SERVER 
    if "SERVER" in os_name or any(server in hostname for server in Server):
        net.add_node(
            node,
            label=hostname,
            title=title,
            color="purple",
            size=40,
            x=150,
            y=300,
            shape="image",
            image="static/icons/server.png",
            physics=False
        )
        net.add_edge(node,"switch2")

    # fortinet/grandstream
    elif "GRANDSTREAMN" in vendor or "FORTINET" in vendor:
        return

    # router
    elif "ZTE" in vendor or "HUAWEITECHNO" in vendor:
        return

    # CAMERA
    elif (
        "554" in ports
        or "8554" in ports
        or "HIKVISION" in vendor
        or "CAMERA" in hostname
    ):
        net.add_node(
            node,
            label=" Camera",
            title=title,
            color="pink",
            size=25,
            shape="image",
            image="static/icons/camera.png",
            physics=False
        )
        net.add_edge("switch1", node)

    # NAS
    elif (
        "QNAP" in vendor
        or "ASUSTEK" in vendor
        or "NAS" in hostname
    ):
        net.add_node(
            node,
            label=" NAS",
            title=title,
            color="brown",
            size=32,
            shape="image",
            image="static/icons/nas.png",
            physics=False
        )
        net.add_edge("switch3", node)

    # PRINTER
    elif any(vendor_prt in vendor for vendor_prt in vendor_printer):
        net.add_node(
            node,
            label=" Printer",
            title=title,
            color="yellow",
            size=28,
            shape="image",
            image="static/icons/printer.png",
            physics=False
        )
        net.add_edge("switch3", node)

    # ACCESS POINT
    elif (
        "OPENWRT" in os_name
        or "AP" in hostname
    ):
        net.add_node(
            node,
            label=" Access Point",
            title=title,
            color="cyan",
            size=30,
            shape="image",
            image="static/icons/access_point.png",
            physics=False
        )
        net.add_edge("switch3", node)

    # IP PHONE
    elif ("5060" in ports or "5061" in ports):
        net.add_node(
            node,
            label=" IP Phone",
            title=title,
            color="green",
            size=28,
            shape="image",
            image="static/icons/phone.png",
            physics=False
        )
        net.add_edge("switch3", node)

    # PC
    elif (
        "WINDOWS" in os_name
        or "DESKTOP" in hostname
        or "PC" in hostname
        or "LAPTOP" in hostname
    ):
        net.add_node(
            node,
            label=hostname,
            title=title,
            color="lime",
            size=28,
            shape="image",
            image="static/icons/pc.png",
            physics=False
        )
        net.add_edge("switch3", node)

    # UNKNOWN
    else:
        net.add_node(
            node,
            label=ip,
            title=title,
            color="lightgray",
            size=25,
            shape="image",
            image="static/icons/unkhown.png",
            physics=False
        )
        net.add_edge("switch3", node)