import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
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
            .outerjoin(Stranka,  Rezervacija.id_stranke  == Stranka.id_stranke)
            .outerjoin(Frizer,   Rezervacija.id_frizerja == Frizer.id_frizer)
            .outerjoin(Salon,    Rezervacija.id_salona   == Salon.id)
            .outerjoin(Storitev, Rezervacija.id_storitve == Storitev.id_storitve)
            .order_by(Rezervacija.datum.desc(), Rezervacija.ura.desc())
            .all()
        )
        return rows
    finally:
        session.close()


def je_termin_zaseden(frizer_id, datum, ura):
    """Vrne True, če ima frizer na ta datum/uro že aktivno rezervacijo."""
    from datetime import date as _date, time as _time
    if isinstance(datum, str):
        datum = _date.fromisoformat(datum)
    if isinstance(ura, str):
        ura = _time.fromisoformat(ura if len(ura) > 5 else ura + ":00")

    session = db.get_session()
    try:
        obstaja = (
            session.query(Rezervacija)
            .filter(
                Rezervacija.id_frizerja == int(frizer_id),
                Rezervacija.datum == datum,
                Rezervacija.ura == ura,
                Rezervacija.status != 'cancelled',
            )
            .first()
        )
        return obstaja is not None
    finally:
        session.close()


def dodaj_rezervacijo(stranka_id, frizer_id, salon_id, storitev_id, datum, ura):
    """
    Doda novo rezervacijo z statusom 'aktiven'. datum in ura sta obvezna.
    """
    from datetime import date as _date, time as _time
    if isinstance(datum, str):
        datum = _date.fromisoformat(datum)
    if isinstance(ura, str):
        ura = _time.fromisoformat(ura if len(ura) > 5 else ura + ":00")

    session = db.get_session()
    try:
        session.add(Rezervacija(
            id_stranke=stranka_id,
            id_frizerja=frizer_id,
            id_salona=salon_id or None,
            id_storitve=storitev_id or None,
            datum=datum,
            ura=ura,
            status='active',
        ))
        session.commit()
    except Exception:
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
    except Exception:
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
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
