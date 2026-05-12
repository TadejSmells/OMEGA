import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import KontaktSporocilo


def get_vsa_sporocila():
    """Vrne vsa kontaktna sporočila, najnovejša najprej."""
    session = db.get_session()
    try:
        return (
            session.query(KontaktSporocilo)
            .order_by(KontaktSporocilo.datum.desc())
            .all()
        )
    finally:
        session.close()


def get_neprebrana_sporocila():
    """Vrne samo neprebrana kontaktna sporočila."""
    session = db.get_session()
    try:
        return (
            session.query(KontaktSporocilo)
            .filter(KontaktSporocilo.prebrano == False)
            .order_by(KontaktSporocilo.datum.desc())
            .all()
        )
    finally:
        session.close()


def dodaj_sporocilo(ime, email, naslov, vsebina):
    """Shrani novo kontaktno sporočilo."""
    session = db.get_session()
    try:
        session.add(KontaktSporocilo(
            ime=ime,
            email=email,
            naslov=naslov,
            vsebina=vsebina
        ))
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def oznaci_kot_prebrano(id_sporocila):
    """Označi sporočilo kot prebrano."""
    session = db.get_session()
    try:
        s = session.query(KontaktSporocilo).filter(
            KontaktSporocilo.id == id_sporocila
        ).first()
        if s:
            s.prebrano = True
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
