import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from models.models import Rezervacija, Stranka, Frizer, Salon, Storitev


def get_vse_rezervacije():
    """Vse rezervacije — za admin pregled."""
    db_session = db.get_session()
    try:
        rows = (
            db_session.query(
                Rezervacija.id_rezervacije,
                (Stranka.ime + ' ' + Stranka.priimek).label('stranka'),
                Frizer.ime.label('frizer'),
                Salon.ime.label('salon'),
                Storitev.ime_storitve.label('storitev'),
                Storitev.cena.label('cena'),
                Storitev.trajanje.label('trajanje'),
                Rezervacija.datum.label('datum'),
                Rezervacija.ura.label('ura')
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
        db_session.close()


def get_rezervacije_za_uporabnika(stranka_id):
    """Rezervacije samo za določeno stranko — za prikaz prijavljenemu uporabniku."""
    db_session = db.get_session()
    try:
        rows = (
            db_session.query(
                Rezervacija.id_rezervacije,
                (Stranka.ime + ' ' + Stranka.priimek).label('stranka'),
                Frizer.ime.label('frizer'),
                Salon.ime.label('salon'),
                Storitev.ime_storitve.label('storitev'),
                Storitev.cena.label('cena'),
                Storitev.trajanje.label('trajanje'),
                Rezervacija.datum.label('datum'),
                Rezervacija.ura.label('ura')
            )
            .outerjoin(Stranka, Rezervacija.id_stranke == Stranka.id_stranke)
            .outerjoin(Frizer, Rezervacija.id_frizerja == Frizer.id_frizer)
            .outerjoin(Salon, Rezervacija.id_salona == Salon.id)
            .outerjoin(Storitev, Rezervacija.id_storitve == Storitev.id_storitve)
            .filter(Rezervacija.id_stranke == stranka_id)
            .order_by(Rezervacija.datum.desc(), Rezervacija.ura.desc())
            .all()
        )
        return rows
    finally:
        db_session.close()


def dodaj_rezervacijo(stranka_id, frizer_id, salon_id, storitev_id, datum=None, ura=None):
    """Doda novo rezervacijo z opcijskim datumom in uro."""
    db_session = db.get_session()
    try:
        db_session.add(Rezervacija(
            id_stranke=stranka_id,
            id_frizerja=frizer_id,
            id_salona=salon_id or None,
            id_storitve=storitev_id or None,
            datum=datum or None,
            ura=ura or None
        ))
        db_session.commit()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()


def izbrisi_rezervacijo(id_rezervacije):
    """Izbriše rezervacijo po ID."""
    db_session = db.get_session()
    try:
        r = db_session.query(Rezervacija).filter(
            Rezervacija.id_rezervacije == id_rezervacije
        ).first()
        if r:
            db_session.delete(r)
            db_session.commit()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()
