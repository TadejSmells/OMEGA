import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from models.models import Rezervacija, Stranka, Frizer, Salon, Storitev


def get_stranka_id_za_user(user_id):
    """Vrne id_stranke za prijavljenega userja, ali None."""
    session = db.get_session()
    try:
        row = session.query(Stranka.id_stranke).filter(
            Stranka.user_id == user_id
        ).first()
        return row[0] if row else None
    finally:
        session.close()


def get_moje_rezervacije(id_stranke):
    """Vrne vse rezervacije prijavljene stranke."""
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
                Rezervacija.datum,
                Rezervacija.ura,
                Rezervacija.status,
                Rezervacija.id_frizerja,
                Rezervacija.id_salona,
                Rezervacija.id_storitve,
            )
            .filter(Rezervacija.id_stranke == id_stranke)
            .outerjoin(Frizer, Rezervacija.id_frizerja == Frizer.id_frizer)
            .outerjoin(Salon, Rezervacija.id_salona == Salon.id)
            .outerjoin(Storitev, Rezervacija.id_storitve == Storitev.id_storitve)
            .order_by(Rezervacija.datum.desc(), Rezervacija.ura.desc())
            .all()
        )
    finally:
        session.close()


def get_mojo_rezervacijo(id_rezervacije, id_stranke):
    """
    Vrne posamezno rezervacijo — SAMO če pripada tej stranki (ownership check).
    Vrne None če ne obstaja ali ni lastnikova.
    """
    session = db.get_session()
    try:
        return (
            session.query(
                Rezervacija.id_rezervacije,
                Rezervacija.id_stranke,
                Rezervacija.id_frizerja,
                Rezervacija.id_salona,
                Rezervacija.id_storitve,
                Rezervacija.datum,
                Rezervacija.ura,
                Rezervacija.status,
            )
            .filter(
                Rezervacija.id_rezervacije == id_rezervacije,
                Rezervacija.id_stranke == id_stranke,   # OWNERSHIP CHECK
            )
            .first()
        )
    finally:
        session.close()


def uredi_mojo_rezervacijo(id_rezervacije, id_stranke, frizer_id, salon_id,
                            storitev_id, datum, ura):
    """
    Posodobi rezervacijo — SAMO če je aktivna in pripada tej stranki.
    Vrne True ob uspehu, False če rezervacija ne obstaja / ni lastnikova / je cancelled.
    """
    session = db.get_session()
    try:
        r = (
            session.query(Rezervacija)
            .filter(
                Rezervacija.id_rezervacije == id_rezervacije,
                Rezervacija.id_stranke == id_stranke,   # OWNERSHIP CHECK
                Rezervacija.status == 'active',          # le aktivne se lahko ureja
            )
            .first()
        )
        if not r:
            return False

        r.id_frizerja = frizer_id or None
        r.id_salona   = salon_id   or None
        r.id_storitve = storitev_id or None
        r.datum       = datum      or r.datum
        r.ura         = ura        or r.ura
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def preklic_moje_rezervacije(id_rezervacije, id_stranke):
    """
    Nastavi status na 'cancelled' — SAMO če je aktivna in pripada tej stranki.
    Vrne True ob uspehu, False sicer.
    """
    session = db.get_session()
    try:
        r = (
            session.query(Rezervacija)
            .filter(
                Rezervacija.id_rezervacije == id_rezervacije,
                Rezervacija.id_stranke == id_stranke,   # OWNERSHIP CHECK
                Rezervacija.status == 'active',
            )
            .first()
        )
        if not r:
            return False
        r.status = 'cancelled'
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_frizerje():
    session = db.get_session()
    try:
        rows = session.query(Frizer).order_by(Frizer.ime).all()
        return [(r.id_frizer, r.ime, r.salon_id) for r in rows]
    finally:
        session.close()


def get_salone():
    session = db.get_session()
    try:
        rows = session.query(Salon).order_by(Salon.ime).all()
        return [(r.id, r.ime, r.naslov, r.mesto) for r in rows]
    finally:
        session.close()


def get_storitve():
    session = db.get_session()
    try:
        rows = session.query(Storitev).order_by(Storitev.ime_storitve).all()
        return [(r.id_storitve, r.ime_storitve, r.cena, r.trajanje) for r in rows]
    finally:
        session.close()
