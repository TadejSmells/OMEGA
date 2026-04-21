import os
import psycopg2

def get_connection():
    """
    Vrne povezavo z bazo podatkov.
    Uporablja okoljske spremenljivke iz .env datoteke.
    
    Primer uporabe v model datotekah:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM frizer")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    """
    conn = psycopg2.connect(
        dbname=os.environ['DBNAME'],
        user=os.environ['DBUSER'],
        password=os.environ['DBPASS'],
        host=os.environ['DBHOST'],
        port=os.environ.get('DBPORT', '5432')
    )
    return conn