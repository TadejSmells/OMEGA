import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import Salon, Frizer, Stranka, Storitev, Urnik, Rezervacija, SaloniInStoritve

# ── DB SETUP ──────────────────────────────────────────────────────────────────

def setup_db():
    import psycopg2
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


# ── INDIVIDUAL GETTERS ────────────────────────────────────────────────────────

def get_frizerje():
    db_session = db.get_session()
    try:
        rows = db_session.query(Frizer).order_by(Frizer.id_frizer).all()
        return [(r.id_frizer, r.salon_id, r.ime, r.kontakt) for r in rows]
    finally:
        db_session.close()


def get_stranke():
    db_session = db.get_session()
    try:
        rows = db_session.query(Stranka).order_by(Stranka.id_stranke).all()
        return [(r.id_stranke, r.ime, r.priimek, r.mail, r.telefon) for r in rows]
    finally:
        db_session.close()


def get_salone():
    db_session = db.get_session()
    try:
        rows = db_session.query(Salon).order_by(Salon.id).all()
        return [(r.id, r.ime, r.naslov, r.mesto, r.telefon) for r in rows]
    finally:
        db_session.close()


def get_storitve():
    db_session = db.get_session()
    try:
        rows = db_session.query(Storitev).order_by(Storitev.id_storitve).all()
        return [(r.id_storitve, r.ime_storitve, r.cena, r.trajanje) for r in rows]
    finally:
        db_session.close()


def get_urnik():
    db_session = db.get_session()
    try:
        rows = (
            db_session.query(Frizer.ime, Urnik.dan, Urnik.ura)
            .join(Frizer, Urnik.id_frizerja == Frizer.id_frizer)
            .order_by(Urnik.dan, Urnik.ura)
            .all()
        )
        return rows
    finally:
        db_session.close()


def get_rezervacije():
    db_session = db.get_session()
    try:
        rows = (
            db_session.query(
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
    finally:
        db_session.close()


def get_saloni_s_storitvami():
    """Single JOIN query — fixes N+1 problem."""
    db_session = db.get_session()
    try:
        saloni = db_session.query(Salon).order_by(Salon.id).all()
        storitve_rows = (
            db_session.query(
                SaloniInStoritve.salon_id,
                Storitev.id_storitve,
                Storitev.ime_storitve,
                Storitev.cena,
                Storitev.trajanje
            )
            .join(Storitev, SaloniInStoritve.storitev_id == Storitev.id_storitve)
            .order_by(SaloniInStoritve.salon_id, Storitev.ime_storitve)
            .all()
        )
        from collections import defaultdict
        storitve_map = defaultdict(list)
        for row in storitve_rows:
            storitve_map[row.salon_id].append(
                (row.id_storitve, row.ime_storitve, row.cena, row.trajanje)
            )
        return [
            {
                'salon': (s.id, s.ime, s.naslov, s.mesto, s.telefon),
                'storitve': storitve_map[s.id]
            }
            for s in saloni
        ]
    finally:
        db_session.close()


def get_storitve_za_salon(salon_id):
    db_session = db.get_session()
    try:
        rows = (
            db_session.query(Storitev)
            .join(SaloniInStoritve, Storitev.id_storitve == SaloniInStoritve.storitev_id)
            .filter(SaloniInStoritve.salon_id == salon_id)
            .order_by(Storitev.ime_storitve)
            .all()
        )
        return [(r.id_storitve, r.ime_storitve, r.cena, r.trajanje) for r in rows]
    finally:
        db_session.close()


# ── GLOBAL SEARCH ─────────────────────────────────────────────────────────────

def iskanje(query):
    """
    Searches salons, hairdressers and services for the query string.
    Case-insensitive partial match. Returns dict with keys:
    saloni, frizerji, storitve.
    """
    if not query or not query.strip():
        return {'saloni': [], 'frizerji': [], 'storitve': []}

    q = f"%{query.strip().lower()}%"
    db_session = db.get_session()
    try:
        from sqlalchemy import func

        saloni = (
            db_session.query(Salon)
            .filter(
                func.lower(Salon.ime).like(q) |
                func.lower(Salon.mesto).like(q) |
                func.lower(Salon.naslov).like(q)
            )
            .order_by(Salon.ime).all()
        )

        frizerji = (
            db_session.query(Frizer)
            .filter(func.lower(Frizer.ime).like(q))
            .order_by(Frizer.ime).all()
        )

        storitve = (
            db_session.query(Storitev)
            .filter(func.lower(Storitev.ime_storitve).like(q))
            .order_by(Storitev.ime_storitve).all()
        )

        return {
            'saloni':   [(s.id, s.ime, s.naslov, s.mesto) for s in saloni],
            'frizerji': [(f.id_frizer, f.ime, f.kontakt) for f in frizerji],
            'storitve': [(s.id_storitve, s.ime_storitve, s.cena) for s in storitve],
        }
    finally:
        db_session.close()


# ── BACKWARDS COMPATIBILITY ───────────────────────────────────────────────────

def get_vse(tip):
    if tip == 'frizer':      return get_frizerje()
    if tip == 'stranka':     return get_stranke()
    if tip == 'salon':       return get_salone()
    if tip == 'storitev':    return get_storitve()
    if tip == 'urnik':       return get_urnik()
    if tip == 'rezervacija': return get_rezervacije()
    return []


# ── INSERTS ───────────────────────────────────────────────────────────────────

def dodaj_rezervacijo(stranka_id, frizer_id, salon_id, storitev_id):
    db_session = db.get_session()
    try:
        db_session.add(Rezervacija(
            id_stranke=stranka_id,
            id_frizerja=frizer_id,
            id_salona=salon_id or None,
            id_storitve=storitev_id or None
        ))
        db_session.commit()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()