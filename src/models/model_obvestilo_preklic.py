import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import db
from models.models import Rezervacija, Stranka, Frizer, Salon, Storitev


def get_zadnja_preklicana_rezervacija(user_id):
    session = db.get_session()

    try:
        stranka = (
            session.query(Stranka.id_stranke)
            .filter(Stranka.user_id == user_id)
            .first()
        )

        if not stranka:
            return None

        row = (
            session.query(
                Rezervacija.id_rezervacije,
                Frizer.ime.label("frizer"),
                Salon.ime.label("salon"),
                Storitev.ime_storitve.label("storitev"),
                Rezervacija.status
            )
            .outerjoin(Frizer, Rezervacija.id_frizerja == Frizer.id_frizer)
            .outerjoin(Salon, Rezervacija.id_salona == Salon.id)
            .outerjoin(Storitev, Rezervacija.id_storitve == Storitev.id_storitve)
            .filter(
                Rezervacija.id_stranke == stranka[0],
                Rezervacija.status == "cancelled"
            )
            .order_by(Rezervacija.id_rezervacije.desc())
            .first()
        )

        return row

    finally:
        session.close()