from datetime import datetime, date, time
from sqlalchemy import Column, Integer, Date, Time, Text
from sqlalchemy.orm import declarative_base, Session
import db
from models.models import Frizer

Base = declarative_base()

class BlokiranTermin(Base):
    __tablename__ = "blokiran_termin"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_frizerja = Column(Integer, nullable=False)
    datum = Column(Date, nullable=False)
    ura_od = Column(Time, nullable=False)
    ura_do = Column(Time, nullable=False)
    razlog = Column(Text, nullable=True)


def get_blokade():
    session: Session = db.get_session()
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
    session: Session = db.get_session()
    try:
        # Convert incoming strings to date/time if necessary
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
    except:
        session.rollback()
        raise
    finally:
        session.close()
