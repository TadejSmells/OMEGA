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


def get_saloni_s_storitvami(priljubljeni_ids=None):
    """
    Optimizirana poizvedba za seznam salonov — odpravlja N+1 problem.

    Args:
        priljubljeni_ids: set of salon IDs the logged-in user has favourited.
                          Favourited salons are sorted to the front of the list.

    Vrne:
        Seznam dict-ov: [{'salon': (id, ime, naslov, mesto, tel),
                          'storitve': [...], 'priljubljen': bool}, ...]
    """
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

        fav_ids = priljubljeni_ids or set()

        rezultat = [
            {
                'salon':       (s.id, s.ime, s.naslov, s.mesto, s.telefon),
                'storitve':    storitve_map[s.id],
                'priljubljen': s.id in fav_ids,
            }
            for s in saloni
        ]

        # Favourited salons float to the top; within each group order is preserved
        rezultat.sort(key=lambda x: 0 if x['priljubljen'] else 1)

        return rezultat
    finally:
        db_session.close()


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


def iskanje(query):
    """
    Išče salone, frizerje in storitve po delnem ujemanju brez upoštevanja velikosti črk.
    Vrne dict z ključi: saloni, frizerji, storitve.
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


def dodaj_salon(ime, naslov, mesto, telefon):
    """
    Doda nov salon v bazo.
    Vrže ValueError če salon s tem imenom že obstaja.
    """
    db_session = db.get_session()
    try:
        obstoječ = db_session.query(Salon).filter(Salon.ime == ime).first()
        if obstoječ:
            raise ValueError(f"Salon z imenom '{ime}' že obstaja.")

        db_session.add(Salon(
            ime=ime,
            naslov=naslov or None,
            mesto=mesto or None,
            telefon=telefon or None
        ))
        db_session.commit()
    except ValueError:
        raise
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()