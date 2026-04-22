import os
import psycopg2
from contextlib import contextmanager
import time

def get_connection():
    """
    Vrne povezavo z bazo podatkov.
    
    Primer uporabe v model datotekah:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM frizer")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    """
    for attempt in range(5):
        try:
            return psycopg2.connect(
                dbname=os.environ['DBNAME'],
                user=os.environ['DBUSER'],
                password=os.environ['DBPASS'],
                host=os.environ['DBHOST'],
                port=os.environ.get('DBPORT', '5432'),
            )
        except psycopg2.OperationalError:
            print(f"DB not ready, retrying ({attempt+1}/5)...")
            time.sleep(2)
    raise RuntimeError("Could not connect to database after 5 attempts")

@contextmanager
def get_cursor():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
        