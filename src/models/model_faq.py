import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from models.models import Faq, KontaktSporocilo

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

def postavi_sporocilo(ime, email, naslov, vsebina):
    session = db.get_session()
    try:
        novo = KontaktSporocilo(
            ime=ime,
            email=email,
            naslov=naslov,
            vsebina=vsebina,
        )
        session.add(novo)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
