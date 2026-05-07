import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from models.models import Rezervacija, Stranka, Frizer, Salon, Storitev


def get_rezervacijo(id_rezervacije):
    session = db.get_session()
    try:
        row = (
            session.query(
                Rezervacija.id_rezervacije,
                Rezervacija.id_stranke,
                Rezervacija.id_frizerja,
                Rezervacija.id_salona,
                Rezervacija.id_storitve,
            )
            .filter(Rezervacija.id_rezervacije == id_rezervacije)
            .first()
        )
        return row
    finally:
        session.close()


def uredi_rezervacijo(id_rezervacije, stranka_id, frizer_id, salon_id, storitev_id):
    session = db.get_session()
    try:
        r = session.query(Rezervacija).filter(
            Rezervacija.id_rezervacije == id_rezervacije
        ).first()
        if r:
            r.id_stranke  = stranka_id
            r.id_frizerja = frizer_id
            r.id_salona   = salon_id or None
            r.id_storitve = storitev_id or None
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
