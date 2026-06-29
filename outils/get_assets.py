import sqlite3
from .get_ip import get_ip

def get_assets():
    conn = sqlite3.connect("network.db")
    network_name = ".".join(get_ip().split(".")[:3])
    cursor = conn.cursor()

    cursor.execute(
    "SELECT * FROM assets WHERE network_name = ?",
    (network_name,)
)

    data = cursor.fetchall()
    conn.close()
    return data 