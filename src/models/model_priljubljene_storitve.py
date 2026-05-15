import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from models.models import PriljubljeneStoritve, Storitev, Stranka


def get_priljubljene_storitve(user_id):
    """
    Vrne seznam priljubljenih storitev za prijavljeno stranko.
    Vsaka vrstica: (id_storitve, ime_storitve, cena, trajanje)
    — enaka oblika kot pri model_cenikstoritev.get_vse_storitve().
    """
    session = db.get_session()
    try:
        rows = (
            session.query(Storitev)
            .join(PriljubljeneStoritve, PriljubljeneStoritve.id_storitve == Storitev.id_storitve)
            .join(Stranka, Stranka.id_stranke == PriljubljeneStoritve.id_stranke)
            .filter(Stranka.user_id == user_id)
            .order_by(Storitev.ime_storitve.asc())
            .all()
        )
        return [(r.id_storitve, r.ime_storitve, r.cena, r.trajanje) for r in rows]
    finally:
        session.close()


def get_priljubljene_ids(user_id):
    """
    Set ID-jev storitev, ki jih ima stranka označene kot priljubljene.
    Uporablja se za prikaz polnega/praznega srčka.
    """
    session = db.get_session()
    try:
        rows = (
            session.query(PriljubljeneStoritve.id_storitve)
            .join(Stranka, Stranka.id_stranke == PriljubljeneStoritve.id_stranke)
            .filter(Stranka.user_id == user_id)
            .all()
        )
        return {row[0] for row in rows}
    finally:
        session.close()