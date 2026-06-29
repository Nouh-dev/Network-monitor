import sqlite3

conn = sqlite3.connect("network.db")

cursor = conn.cursor()

cursor.execute("""
            CREATE TABLE IF NOT EXISTS assets (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               ip TEXT UNIQUE,
               mac TEXT,
               hostname TEXT,
               status TEXT,
               os_name TEXT,
               vendor TEXT,
               ports TEXT,
               status_port TEXT,
               wifi TEXT,
               network_name TEXT
                )  
""")


def save_device(ip,mac,hostname,status,os_name,vendor,ports,status_port,network):
    conn = sqlite3.connect("network.db")

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM assets WHERE ip=? ",(ip,))
    exists = cursor.fetchone()

    if exists:
        cursor.execute("""
                        UPDATE assets
                        SET mac = ? ,hostname = ?,status = ?,os_name = ? ,vendor=?, ports = ?, status_port=? , network_name = ?
                        WHERE ip=? """,(mac, hostname, status,os_name, vendor, ports, status_port,network, ip))
    
    else:
        cursor.execute(""" 
                    INSERT INTO assets(ip,mac,hostname,status,os_name,vendor,ports,status_port,network_name)
                    VALUES (?,?,?,?,?,?,?,?,?)""",(ip,mac,hostname,status,os_name,vendor,ports,status_port,network))
    conn.commit()
    conn.close()


conn.commit()
conn.close()
