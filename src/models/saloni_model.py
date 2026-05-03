import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import db
from models.models import Salon, Storitev

def get_saloni():
    session = db.get_session()
    try:
        rows = session.query(Salon).order_by(Salon.id).all()
        return [(r.id, r.ime, r.naslov, r.mesto, r.telefon) for r in rows]
    finally:
        session.close()


def get_storitve_za_salon(salon_id):
    session = db.get_session()
    try:
        rows = (
            session.query(Storitev)
            .join(Storitev.saloni)  # predpostavlja relacijo many-to-many ali FK
            .filter(Salon.id == salon_id)
            .all()
        )
        return [(r.id_storitve, r.ime_storitve, r.cena, r.trajanje) for r in rows]
    finally:
        session.close()