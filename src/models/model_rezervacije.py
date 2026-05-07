import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from datetime import date
from models.models import Rezervacija, Stranka, Frizer, Salon, Storitev


def get_vse_rezervacije():
    session = db.get_session()
    try:
        rows = (
            session.query(
                Rezervacija.id_rezervacije,
                (Stranka.ime + ' ' + Stranka.priimek).label('stranka'),
                Frizer.ime.label('frizer'),
                Salon.ime.label('salon'),
                Storitev.ime_storitve.label('storitev'),
                Rezervacija.datum,
                Rezervacija.ura,
                Storitev.cena.label('cena'),
                Rezervacija.status,
            )
            .outerjoin(Stranka, Rezervacija.id_stranke == Stranka.id_stranke)
            .outerjoin(Frizer, Rezervacija.id_frizerja == Frizer.id_frizer)
            .outerjoin(Salon, Rezervacija.id_salona == Salon.id)
            .outerjoin(Storitev, Rezervacija.id_storitve == Storitev.id_storitve)
            .order_by(Rezervacija.datum.desc(), Rezervacija.ura.desc())
            .all()
        )
        return rows
    finally:
        session.close()


def dodaj_rezervacijo(stranka_id, frizer_id, salon_id, storitev_id):
    session = db.get_session()
    try:
        session.add(Rezervacija(
            id_stranke=stranka_id,
            id_frizerja=frizer_id,
            id_salona=salon_id or None,
            id_storitve=storitev_id or None
        ))
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def izbrisi_rezervacijo(id_rezervacije):
    session = db.get_session()
    try:
        r = session.query(Rezervacija).filter(
            Rezervacija.id_rezervacije == id_rezervacije
        ).first()
        if r:
            session.delete(r)
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def preklic_rezervacije(id_rezervacije):
    session = db.get_session()
    try:
        r = session.query(Rezervacija).filter(
            Rezervacija.id_rezervacije == id_rezervacije
        ).first()
        if r:
            r.status = 'cancelled'
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()