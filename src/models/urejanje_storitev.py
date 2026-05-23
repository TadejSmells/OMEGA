import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime, time as Time
from decimal import Decimal, InvalidOperation

import db
from models.models import Storitev


def get_storitev(id_storitve):
    """Vrne podatke o eni storitvi."""
    session = db.get_session()

    try:
        s = session.query(Storitev).filter(Storitev.id_storitve == id_storitve).first()

        if s is None:
            return None

        return {
            "id": s.id_storitve,
            "naziv": s.ime_storitve,
            "cena": s.cena,
            "trajanje": s.trajanje,
            "opis": s.opis
        }

    finally:
        session.close()


def _parse_trajanje(vrednost):
    if not vrednost and vrednost != 0:
        return None

    v = str(vrednost).strip()
    if not v:
        return None

    # Format HH:MM:SS ali HH:MM
    if ':' in v:
        try:
            parts = v.split(':')
            h, m, s = int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0
            return Time(h, m, s)
        except (ValueError, IndexError):
            raise ValueError("Trajanje ni v veljavni obliki (pričakovano HH:MM:SS).")

    # Plain minute
    try:
        mins = int(v)
        return Time(mins // 60, mins % 60)
    except ValueError:
        raise ValueError("Trajanje ni veljavno.")


def update_storitev(storitev_id, naziv, cena, trajanje, opis):
    if not naziv or not naziv.strip():
        raise ValueError("Naziv storitve je obvezen.")

    # Pretvori ceno v Decimal
    cena_val = None
    if cena and str(cena).strip():
        try:
            cena_val = Decimal(str(cena).strip())
        except InvalidOperation:
            raise ValueError("Cena ni veljavna številka.")

    trajanje_val = _parse_trajanje(trajanje)

    session = db.get_session()

    try:
        s = session.query(Storitev).filter(Storitev.id_storitve == storitev_id).first()

        if s is None:
            return False

        s.ime_storitve = naziv.strip()
        s.cena = cena_val
        s.trajanje = trajanje_val
        s.opis = (opis or "").strip() or None

        session.commit()

        return True

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()