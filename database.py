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
               vendor TEXT
                )  
""")


def save_device(ip,mac,hostname,status,vendor):
    conn = sqlite3.connect("network.db")

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM assets WHERE ip=? ",(ip,))
    exists = cursor.fetchone()

    if exists:
        cursor.execute("""
                        UPDATE assets
                        SET mac = ? ,hostname = ?,status = ?,vendor=?
                        WHERE ip=? """,(ip,mac,hostname,status,vendor))
    
    else:
        cursor.execute(""" 
                    INSERT INTO assets(ip,mac,hostname,status,vendor)
                    VALUES (?,?,?,?,?)""",(ip,mac,hostname,status,vendor))
    conn.commit()
    conn.close()


conn.commit()
conn.close()
