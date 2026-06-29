import sqlite3

def get_device_from_db(ip):
    conn = sqlite3.connect("network.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT hostname, os_name, vendor, ports, status_port
        FROM assets
        WHERE ip = ?
    """, (ip,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "hostname": row[0],
            "os_name": row[1],
            "vendor": row[2],
            "ports": row[3],
            "status_port": row[4]
        }

    return None