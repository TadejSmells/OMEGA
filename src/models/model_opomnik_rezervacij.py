import db
from datetime import date
from models.models import Rezervacija, Stranka, Frizer, Salon, Storitev


def get_danasnje_rezervacije_frizerja(user_id):
    """
    Vrne aktivne rezervacije frizerja za danaÅ¡nji dan,
    glede na user_id (iz session).
    """
    session = db.get_session()
    try:
        danes = date.today()

        frizer = session.query(Frizer).filter(
            Frizer.user_id == user_id
        ).first()

        if not frizer:
            return []

        rows = (
            session.query(
                Rezervacija.id_rezervacije,
                Rezervacija.ura,
                (Stranka.ime + ' ' + Stranka.priimek).label('stranka'),
                Salon.ime.label('salon'),
                Storitev.ime_storitve.label('storitev'),
            )
            .filter(
                Rezervacija.id_frizerja == frizer.id_frizer,
                Rezervacija.datum == danes,
                Rezervacija.status == 'active'
            )
            .outerjoin(Stranka,  Rezervacija.id_stranke  == Stranka.id_stranke)
            .outerjoin(Salon,    Rezervacija.id_salona   == Salon.id)
            .outerjoin(Storitev, Rezervacija.id_storitve == Storitev.id_storitve)
            .order_by(Rezervacija.ura)
            .all()
        )
        return rows
    finally:
        session.close()