import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db

def get_vse_storitve():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM storitev;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows