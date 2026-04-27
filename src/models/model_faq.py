import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from models.models import Faq

def pridobi_faq ():
    session = db.get_session()
    try:
        rows = (
            session.query(
                Faq.id_faq,
                Faq.vprasanje,
                Faq.odgovor
            )
            .filter(Faq.aktiven == True)
            .order_by(Faq.vrstni_red, Faq.id_faq)
            .all()
        )
        return rows
    finally:
        session.close()

