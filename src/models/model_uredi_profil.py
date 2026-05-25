from db import Session
from db import Session
from models.models import Stranka   # adjust path to match your actual file
from models.models import Frizer

def get_stranka_by_user(user_id):
    with Session() as s:
        return s.query(Stranka).filter_by(user_id=user_id).first()

def get_frizer_by_user(user_id):
    with Session() as s:
        return s.query(Frizer).filter_by(user_id=user_id).first()

def uredi_stranko(user_id, ime, priimek, mail, telefon):
    with Session() as s:
        stranka = s.query(Stranka).filter_by(user_id=user_id).first()
        if not stranka:
            return False, "Stranka ni najdena."
        stranka.ime     = ime
        stranka.priimek = priimek
        stranka.mail    = mail
        stranka.telefon = telefon
        s.commit()
        return True, "Podatki so bili posodobljeni."

def uredi_frizerja(user_id, ime, kontakt):
    with Session() as s:
        frizer = s.query(Frizer).filter_by(user_id=user_id).first()
        if not frizer:
            return False, "Frizer ni najden."
        frizer.ime     = ime
        frizer.kontakt = kontakt
        s.commit()
        return True, "Podatki so bili posodobljeni."