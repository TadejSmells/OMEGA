import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sqlalchemy import func
import db
from models.models import Sporocilo, Stranka

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