import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sqlalchemy import func
import db
from models.models import Sporocilo, Stranka, Frizer

def seznam_sporocil(id_frizerja):
    session = db.get_session()
    try:
        return (
            session.query(
                Sporocilo.id,
                Sporocilo.naslov,
                Sporocilo.vsebina,
                Sporocilo.datum,
                Sporocilo.prebrano,
                func.concat(Stranka.ime, ' ', Stranka.priimek).label('ime'),
                Stranka.mail.label('email'),
            )
            .outerjoin(Stranka, Sporocilo.id_stranke == Stranka.id_stranke)
            .filter(Sporocilo.id_frizerja == id_frizerja)
            .order_by(Sporocilo.id.desc())
            .all()
        )
    finally:
        session.close()


def podrobnosti_sporocila(id):
    session = db.get_session()
    try:
        return (
            session.query(
                Sporocilo.id,
                Sporocilo.id_frizerja,
                Sporocilo.naslov,
                Sporocilo.vsebina,
                Sporocilo.datum,
                Sporocilo.prebrano,
                func.concat(Stranka.ime, ' ', Stranka.priimek).label('ime'),
                Stranka.mail.label('email'),
            )
            .outerjoin(Stranka, Sporocilo.id_stranke == Stranka.id_stranke)
            .filter(Sporocilo.id == id)
            .first()
        )
    finally:
        session.close()

def get_sporocila_frizerja(frizer_id):
    session = db.get_session()
    try:
        return (
            session.query(
                Sporocilo.id,
                Sporocilo.vsebina,
                Stranka.ime,
                Stranka.priimek
            )
            .join(Stranka, Sporocilo.id_stranke == Stranka.id_stranke)
            .filter(Sporocilo.id_frizerja == frizer_id)
            .order_by(Sporocilo.id.desc())
            .all()
        )
    finally:
        session.close()


# ── NOVO: STRANKA POŠLJE SPOROČILO FRIZERJU ──────────────────────────────────

def poslji_sporocilo(id_stranke, id_frizerja, naslov, vsebina):
    """
    Ustvari novo sporočilo stranke za danega frizerja.
    Vrne id novega sporočila. Sproži ValueError ob neveljavnih podatkih.
    """
    naslov = (naslov or '').strip()
    vsebina = (vsebina or '').strip()
    if not vsebina:
        raise ValueError("Sporočilo je prazno.")
    if not naslov:
        naslov = "(brez naslova)"

    session = db.get_session()
    try:
        # frizer mora obstajati
        frizer = session.query(Frizer).filter(Frizer.id_frizer == id_frizerja).first()
        if frizer is None:
            raise ValueError("Frizer ne obstaja.")

        sporocilo = Sporocilo(
            id_stranke=id_stranke,
            id_frizerja=id_frizerja,
            naslov=naslov[:200],
            vsebina=vsebina,
            prebrano=False,
        )
        session.add(sporocilo)
        session.commit()
        return sporocilo.id
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ── NOVO: OZNAČI SPOROČILO KOT PREBRANO ──────────────────────────────────────

def oznaci_prebrano(id_sporocila, id_frizerja):
    """
    Označi sporočilo kot prebrano — samo če pripada danemu frizerju.
    Vrne True ob uspehu, False če sporočilo ni najdeno / ne pripada frizerju.
    """
    session = db.get_session()
    try:
        sporocilo = (
            session.query(Sporocilo)
            .filter(
                Sporocilo.id == id_sporocila,
                Sporocilo.id_frizerja == id_frizerja,
            )
            .first()
        )
        if sporocilo is None:
            return False
        if not sporocilo.prebrano:
            sporocilo.prebrano = True
            session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
