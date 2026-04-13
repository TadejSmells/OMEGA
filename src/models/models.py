from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Frizer(Base):
    __tablename__ = 'frizer'
    id_frizer  = Column(Integer, primary_key=True)
    salon_id   = Column(Integer, nullable=True)
    ime        = Column(String(100))
    kontakt    = Column(String(50))

class Stranka(Base):
    __tablename__ = 'stranka'
    id_stranke = Column(Integer, primary_key=True)
    ime        = Column(String(100))
    priimek    = Column(String(100))
    mail       = Column(String(150))
    telefon    = Column(String(50))

class Rezervacija(Base):
    __tablename__ = 'rezervacija'
    id_rezervacije = Column(Integer, primary_key=True)
    id_stranke     = Column(Integer, ForeignKey('stranka.id_stranke'))
    id_frizerja    = Column(Integer, ForeignKey('frizer.id_frizer'))