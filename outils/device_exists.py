import sqlite3

def device_exists(ip):
    conn = sqlite3.connect("network.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM assets WHERE ip = ?", (ip,))
    exists = cursor.fetchone()

    conn.close()

    return exists is not None