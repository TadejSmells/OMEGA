import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from models.models import Storitev

def get_vse_storitve():
    session = db.get_session()
    try:
        rows = session.query(Storitev).order_by(Storitev.id_storitve).all()
        return [(r.id_storitve, r.ime_storitve, r.cena, r.trajanje) for r in rows]
    finally:
        session.close()