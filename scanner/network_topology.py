from pyvis.network import Network


def network_topologyy():

    net = Network(height="800px", width="100%", bgcolor="white")

    net.set_options("""
    var options = {
    "layout": {
        "hierarchical": {
        "enabled": false,
        "direction": "UD",
        "sortMethod": "directed",
        "levelSeparation": 180,
        "nodeSpacing": 150
        }
    },
    "physics": {
        "enabled": true
    },
    "interaction": {
        "zoomView": false,
        "dragView": false,
        "keyboard": false,
        "dragNodes": false
  }
    }
    """)

    net.add_node("internet",
                  label=" Internet", 
                  color="gray",
                  shape="image",
                  size = 30 ,
                  image = "static/icons/internet.png",
                  x=0, y =-800,
                  physics = False)

    net.add_node("router",
                 label=" Router",
                 color="gray",
                 size=30,
                 shape="image",
                 image = "static/icons/router.png",
                 x=0, y = -550,
                 physics = False) 
    
    net.add_node("grandstream",
                 label="Grandstream",
                 color="gray",
                 size=60,
                 shape="image",
                title = """ 
                IP : 192.168.10.1
                MAC : 00:0b:82:e0:8b:2b
                Hostname : GrandstreamN
                Vendor : 
                OS : 
                Ports : 22 ssh , 53 domain , 80 http , 443 https , 445 microsoft-ds  """ ,
                 image = "static/icons/grandstream.png",
                 x=350, y = -250,
                 physics = False) 
    
    net.add_node("firewall",
                 label=" Fortinet",
                 color="red",
                 size=30,
                 shape="image",
                 title = f"""
                 IP : 10.10.10.5
                 MAC : 94:ff:3c:66:e9:7c
                 Hostname : None
                 Status : Online
                 Vendor : Fortinet
                 OS : Unknown
                 Ports :
                 - 80 (HTTP)
                 - 443 (HTTPS)

                 Device Type : Firewall
                """,
                 x=-350, y = -250,
                 image = "static/icons/firewall.png",
                 physics = False) 

    net.add_node("switch1",
                 label=" Switch 1",
                 color="blue",
                 shape="image",
                 image = "static/icons/switch.png",
                 x=-350, y = 50,
                 physics = False) 
    
    net.add_node("switch2", 
                 label=" Switch 2", 
                 color="blue",
                 shape="image",
                 image = "static/icons/switch.png",
                 x=-350, y = 150,
                 physics = False) 
    
    net.add_node("switch3", 
                 label=" Switch 3", 
                 color="blue",
                 shape="image",
                 image = "static/icons/switch.png",
                 x=-350, y = 250,
                 physics = False) 

    net.add_edge("internet","router")
    net.add_edge("router","grandstream")
    net.add_edge("router","firewall")
    net.add_edge("firewall","switch1")
    net.add_edge("switch1","switch2")
    net.add_edge("switch2","switch3")
    net.add_edge("grandstream","switch1")

    return net