from datetime import datetime, date, time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import BlokiranTermin, Frizer


def get_blokade():
    session = db.get_session()
    try:
        return (
            session.query(BlokiranTermin, Frizer)
            .join(
                Frizer,
                BlokiranTermin.id_frizerja == Frizer.id_frizer
            )
            .order_by(
                BlokiranTermin.datum.desc(),
                BlokiranTermin.ura_od.desc()
            )
            .all()
        )
    finally:
        session.close()


def dodaj_blokado(frizer_id, datum, ura_od, ura_do, razlog):
    session = db.get_session()
    try:
        if isinstance(datum, str):
            datum = datetime.fromisoformat(datum).date()
        if isinstance(ura_od, str):
            ura_od = time.fromisoformat(ura_od)
        if isinstance(ura_do, str):
            ura_do = time.fromisoformat(ura_do)

        t = BlokiranTermin(
            id_frizerja=int(frizer_id),
            datum=datum,
            ura_od=ura_od,
            ura_do=ura_do,
            razlog=razlog
        )
        session.add(t)
        session.commit()
        session.refresh(t)
        return t
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
