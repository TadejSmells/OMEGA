import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from models.models import Stranka, Rezervacija, Frizer

def get_stranka(id_stranke):
    """Vrne vse kontaktne podatke posamezne stranke."""
    session = db.get_session()
    try:
        return (
            session.query(
                Stranka.id_stranke,
                Stranka.ime,
                Stranka.priimek,
                Stranka.mail,
                Stranka.telefon,
            )
            .filter(Stranka.id_stranke == id_stranke)
            .first()
        )
    finally:
        session.close()


def get_stranke_frizerja(user_id):
    session_db = db.get_session()

    try:
        frizer = session_db.query(Frizer).filter(
            Frizer.user_id == user_id
        ).first()

        if not frizer:
            return []

        return (
            session_db.query(
                Stranka.id_stranke,
                Stranka.ime,
                Stranka.priimek,
                Stranka.mail,
                Stranka.telefon,
            )
            .join(Rezervacija, Rezervacija.id_stranke == Stranka.id_stranke)
            .filter(Rezervacija.id_frizerja == frizer.id_frizer)
            .distinct()
            .all()
        )

    finally:
        session_db.close()