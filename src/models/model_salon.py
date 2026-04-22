import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import Salon, Frizer, Stranka, Storitev, Urnik, Rezervacija, SaloniInStoritve

# ── DB SETUP ──────────────────────────────────────────────────────────────────
# setup_db in polni_db ostaneta z raw SQL
def setup_db():
    import psycopg2
    from urllib.parse import quote_plus
    conn = psycopg2.connect(
        dbname=os.environ['DBNAME'],
        user=os.environ['DBUSER'],
        password=os.environ['DBPASS'],
        host=os.environ['DBHOST'],
        port=os.environ.get('DBPORT', '5432')
    )
    conn.autocommit = True
    cursor = conn.cursor()
    sql_path = os.path.join(os.path.dirname(__file__), '..', 'creation.sql')
    with open(sql_path, 'r') as f:
        sql = f.read()
    cursor.execute(sql)
    cursor.close()
    conn.close()
    return True


def polni_db():
    import psycopg2
    conn = psycopg2.connect(
        dbname=os.environ['DBNAME'],
        user=os.environ['DBUSER'],
        password=os.environ['DBPASS'],
        host=os.environ['DBHOST'],
        port=os.environ.get('DBPORT', '5432')
    )
    cursor = conn.cursor()
    sql_path = os.path.join(os.path.dirname(__file__), '..', 'testni_podatki.sql')
    with open(sql_path, 'r') as f:
        sql = f.read()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return True

# ── GETTERS ───────────────────────────────────────────────────────────────────

def get_vse(tip):
    session = db.get_session()
    try:
        if tip == 'frizer':
            rows = session.query(Frizer).order_by(Frizer.id_frizer).all()
            return [(r.id_frizer, r.salon_id, r.ime, r.kontakt) for r in rows]
        elif tip == 'stranka':
            rows = session.query(Stranka).order_by(Stranka.id_stranke).all()
            return [(r.id_stranke, r.ime, r.priimek, r.mail, r.telefon) for r in rows]
        elif tip == 'rezervacija':
            rows = (
                session.query(
                    Rezervacija.id_rezervacije,
                    (Stranka.ime + ' ' + Stranka.priimek).label('stranka'),
                    Frizer.ime.label('frizer'),
                    Salon.ime.label('salon'),
                    Storitev.ime_storitve.label('storitev')
                )
                .outerjoin(Stranka, Rezervacija.id_stranke == Stranka.id_stranke)
                .outerjoin(Frizer, Rezervacija.id_frizerja == Frizer.id_frizer)
                .outerjoin(Salon, Rezervacija.id_salona == Salon.id)
                .outerjoin(Storitev, Rezervacija.id_storitve == Storitev.id_storitve)
                .order_by(Rezervacija.id_rezervacije)
                .all()
            )
            return rows
        elif tip == 'salon':
            rows = session.query(Salon).order_by(Salon.id).all()
            return [(r.id, r.ime, r.naslov, r.mesto, r.telefon) for r in rows]
        elif tip == 'storitev':
            rows = session.query(Storitev).order_by(Storitev.id_storitve).all()
            return [(r.id_storitve, r.ime_storitve, r.cena, r.trajanje) for r in rows]
        elif tip == 'urnik':
            rows = (
                session.query(Frizer.ime, Urnik.dan, Urnik.ura)
                .join(Frizer, Urnik.id_frizerja == Frizer.id_frizer)
                .order_by(Urnik.dan, Urnik.ura)
                .all()
            )
            return rows
        return []
    finally:
        session.close()


def get_storitve_za_salon(salon_id):
    session = db.get_session()
    try:
        rows = (
            session.query(Storitev)
            .join(SaloniInStoritve, Storitev.id_storitve == SaloniInStoritve.storitev_id)
            .filter(SaloniInStoritve.salon_id == salon_id)
            .order_by(Storitev.ime_storitve)
            .all()
        )
        return [(r.id_storitve, r.ime_storitve, r.cena, r.trajanje) for r in rows]
    finally:
        session.close()

# ── INSERTS ───────────────────────────────────────────────────────────────────

def dodaj_rezervacijo(stranka_id, frizer_id, salon_id, storitev_id):
    session = db.get_session()
    try:
        session.add(Rezervacija(
            id_stranke=stranka_id,
            id_frizerja=frizer_id,
            id_salona=salon_id or None,
            id_storitve=storitev_id or None
        ))
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()