import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from models.models import Stranka, Rezervacija, Frizer, Salon, Storitev


def get_vse_stranke():
    """Vrne seznam vseh strank (id, ime, priimek)."""
    session = db.get_session()
    try:
        rows = session.query(Stranka).order_by(Stranka.id_stranke).all()
        return [(r.id_stranke, r.ime, r.priimek) for r in rows]
    finally:
        session.close()


def get_rezervacije_stranke(id_stranke):
    """Vrne vse rezervacije posamezne stranke."""
    session = db.get_session()
    try:
        return (
            session.query(
                Rezervacija.id_rezervacije,
                Frizer.ime.label('frizer'),
                Salon.ime.label('salon'),
                Storitev.ime_storitve.label('storitev'),
                Storitev.cena.label('cena'),
                Storitev.trajanje.label('trajanje'),
            )
            .filter(Rezervacija.id_stranke == id_stranke)
            .outerjoin(Frizer, Rezervacija.id_frizerja == Frizer.id_frizer)
            .outerjoin(Salon, Rezervacija.id_salona == Salon.id)
            .outerjoin(Storitev, Rezervacija.id_storitve == Storitev.id_storitve)
            .order_by(Rezervacija.id_rezervacije.desc())
            .all()
        )
    finally:
        session.close()


def get_rezervacije_uporabnika(user_id):

    session_db = db.get_session()

    try:
        return (
            session_db.query(
                Rezervacija.id_rezervacije,
                Frizer.ime.label('frizer'),
                Salon.ime.label('salon'),
                Storitev.ime_storitve.label('storitev'),
                Storitev.cena.label('cena'),
                Storitev.trajanje.label('trajanje'),
            )
            .join(Stranka, Rezervacija.id_stranke == Stranka.id_stranke)
            .filter(Stranka.user_id == user_id)
            .outerjoin(Frizer, Rezervacija.id_frizerja == Frizer.id_frizer)
            .outerjoin(Salon, Rezervacija.id_salona == Salon.id)
            .outerjoin(Storitev, Rezervacija.id_storitve == Storitev.id_storitve)
            .all()
        )

    finally:
        session_db.close()