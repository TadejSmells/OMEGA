import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from datetime import date
from models.models import Rezervacija, Stranka, Frizer, Salon, Storitev


def get_danasnje_rezervacije_stranke(user_id):
    """
    Vrne aktivne rezervacije stranke za danaÅ¡nji dan,
    glede na user_id (iz session).
    """
    session = db.get_session()
    try:
        danes = date.today()

        stranka = session.query(Stranka).filter(
            Stranka.user_id == user_id
        ).first()

        if not stranka:
            return []

        rows = (
            session.query(
                Rezervacija.id_rezervacije,
                Rezervacija.ura,
                Frizer.ime.label('frizer'),
                Salon.ime.label('salon'),
                Storitev.ime_storitve.label('storitev'),
            )
            .filter(
                Rezervacija.id_stranke == stranka.id_stranke,
                Rezervacija.datum == danes,
                Rezervacija.status == 'active'
            )
            .outerjoin(Frizer,  Rezervacija.id_frizerja == Frizer.id_frizer)
            .outerjoin(Salon,   Rezervacija.id_salona   == Salon.id)
            .outerjoin(Storitev, Rezervacija.id_storitve == Storitev.id_storitve)
            .order_by(Rezervacija.ura)
            .all()
        )
        return rows
    finally:
        session.close()