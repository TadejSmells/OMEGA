from db import db
from datetime import datetime


class Sporocilo(db.Model):
    __tablename__ = "sporocila"

    id = db.Column(db.Integer, primary_key=True)

    ime = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    naslov = db.Column(db.String(200), nullable=False)
    vsebina = db.Column(db.Text, nullable=False)

    datum = db.Column(db.DateTime, default=datetime.utcnow)

    prebrano = db.Column(db.Boolean, default=False)