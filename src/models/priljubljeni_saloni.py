import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import db
from models.models import PriljubljeniSaloni

def get_priljubljeni(id_stranke):
    session = db.get_session()
    try:
        rows = session.query(PriljubljeniSaloni)\
            .filter(PriljubljeniSaloni.id_stranke == id_stranke)\
            .all()
        return [r.id_salona for r in rows]
    finally:
        session.close()

def toggle_priljubljenega(id_stranke, id_salona):
    session = db.get_session()
    try:
        obstaja = session.query(PriljubljeniSaloni)\
            .filter(
                PriljubljeniSaloni.id_stranke == id_stranke,
                PriljubljeniSaloni.id_salona == id_salona
            ).first()

        if obstaja:
            session.delete(obstaja)
        else:
            nov = PriljubljeniSaloni(id_stranke=id_stranke, id_salona=id_salona)
            session.add(nov)

        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()