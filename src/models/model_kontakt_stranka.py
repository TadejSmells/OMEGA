import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from models.models import Stranka, Rezervacija, Frizer


def get_vse_kontakti():
    """Vrne seznam vseh strank (id, ime, priimek)."""
    session = db.get_session()
    try:
        rows = session.query(Stranka).order_by(Stranka.id_stranke).all()
        return [(r.id_stranke, r.ime, r.priimek) for r in rows]
    finally:
        session.close()


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
        return (
            session_db.query(
                Stranka.ime,
                Stranka.priimek,
                Stranka.mail,
                Stranka.telefon,
            )
            .join(Rezervacija,
                  Rezervacija.id_stranke == Stranka.id_stranke)
            .join(Frizer,
                  Rezervacija.id_frizerja == Frizer.id_frizer)
            .filter(Frizer.user_id == user_id)
            .distinct()
            .all()
        )

    finally:
        session_db.close()