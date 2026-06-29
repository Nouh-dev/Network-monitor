from flask import Flask , render_template
from scanner.scanner_network import scanner
from outils.get_ip import get_ip
from outils.get_assets import get_assets
from scanner.network_topology import network_topologyy
app = Flask(__name__)



@app.route("/")
def home():
    devices = get_assets()
    return render_template("base.html", devices=devices)


@app.route("/scan")
def scan():
    ip = get_ip()
    scanner(ip)
    return "OK"

@app.route("/cartographie")
def schéma():
    return render_template("network.html")

app.run(debug=True)

