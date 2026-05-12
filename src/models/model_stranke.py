import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import db
from models.models import Stranka
from sqlalchemy import text


def get_stranko(id_stranke):
    session = db.get_session()

    try:
        row = (
            session.query(
                Stranka.id_stranke,
                Stranka.ime,
                Stranka.priimek,
                Stranka.mail,
                Stranka.telefon,
                Stranka.id_naj_frizer
            )
            .filter(Stranka.id_stranke == id_stranke)
            .first()
        )
        return row

    finally:
        session.close()


def get_vse_stranke():
    session = db.get_session()

    try:
        rows = (
            session.query(
                Stranka.id_stranke,
                Stranka.ime,
                Stranka.priimek,
                Stranka.mail,
                Stranka.telefon,
                Stranka.id_naj_frizer
            )
            .all()
        )
        return rows

    finally:
        session.close()


def uredi_stranko(id_stranke, ime, priimek, mail, telefon, id_naj_frizer):
    session = db.get_session()

    try:
        s = (
            session.query(Stranka)
            .filter(Stranka.id_stranke == id_stranke)
            .first()
        )

        if s:
            s.ime = ime
            s.priimek = priimek
            s.mail = mail
            s.telefon = telefon
            s.id_naj_frizer = id_naj_frizer or None
            session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def izbrisi_stranko(id_stranke):
    session = db.get_session()

    try:
        # First delete linked reservations
        session.execute(
            text("DELETE FROM rezervacija WHERE id_stranke = :id"),
            {"id": id_stranke}
        )

        # Then delete the customer
        session.query(Stranka).filter(
            Stranka.id_stranke == id_stranke
        ).delete()

        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()