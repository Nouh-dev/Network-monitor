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
               status_port TEXT
                )  
""")


def save_device(ip,mac,hostname,status,vendor,ports,status_port,os_name):
    conn = sqlite3.connect("network.db")

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM assets WHERE ip=? ",(ip,))
    exists = cursor.fetchone()

    if exists:
        cursor.execute("""
                        UPDATE assets
                        SET mac = ? ,hostname = ?,status = ?,os_name = ? ,vendor=?, ports = ?, status_port=?
                        WHERE ip=? """,(mac, hostname, status,os_name, vendor, ports, status_port, ip))
    
    else:
        cursor.execute(""" 
                    INSERT INTO assets(ip,mac,hostname,status,os_name,vendor,ports,status_port)
                    VALUES (?,?,?,?,?,?,?,?)""",(ip,mac,hostname,status,os_name,vendor,ports,status_port))
    conn.commit()
    conn.close()


conn.commit()
conn.close()
