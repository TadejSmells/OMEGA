import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import Rezervacija, Stranka, Salon, Storitev


def get_rezervacije_frizerja(frizer_id):
    """Vrne vse aktivne rezervacije za določenega frizerja."""
    session = db.get_session()
    try:
        rows = (
            session.query(
                Rezervacija.id_rezervacije,
                (Stranka.ime + ' ' + Stranka.priimek).label('stranka'),
                Storitev.ime_storitve.label('storitev'),
                Salon.ime.label('salon'),
                Rezervacija.datum,
                Rezervacija.ura,
                Rezervacija.status,
            )
            .outerjoin(Stranka,  Rezervacija.id_stranke  == Stranka.id_stranke)
            .outerjoin(Storitev, Rezervacija.id_storitve == Storitev.id_storitve)
            .outerjoin(Salon,    Rezervacija.id_salona   == Salon.id)
            .filter(Rezervacija.id_frizerja == frizer_id)
            .order_by(Rezervacija.datum.desc(), Rezervacija.ura.desc())
            .all()
        )
        return rows
    finally:
        session.close()


def preklic_rezervacije_frizerja(id_rezervacije, frizer_id):
    """
    Nastavi status rezervacije na 'cancelled'.
    Vrne True če je preklic uspel, False če rezervacija ne pripada temu frizerju.
    """
    session = db.get_session()
    try:
        r = session.query(Rezervacija).filter(
            Rezervacija.id_rezervacije == id_rezervacije,
            Rezervacija.id_frizerja    == frizer_id
        ).first()
        if r is None:
            return False
        r.status = 'cancelled'
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
