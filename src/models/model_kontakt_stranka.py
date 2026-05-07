import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from models.models import Stranka


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