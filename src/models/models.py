from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, Time, Text, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# TA DATOTEKA DEFINIRA STRUKTURO BAZE PODATKOV (vse tabele)
# Stolpci se ujemajo s creation.sql

class Salon(Base):
    __tablename__ = 'salon'
    id      = Column(Integer, primary_key=True)
    ime     = Column(String(100), nullable=False)
    naslov  = Column(Text)
    mesto   = Column(String(100))
    telefon = Column(String(100))

class Frizer(Base):
    __tablename__ = 'frizer'
    id_frizer = Column(Integer, primary_key=True)
    salon_id  = Column(Integer, ForeignKey('salon.id'), nullable=True)
    ime       = Column(String(100))
    kontakt   = Column(String(100))

class Stranka(Base):
    __tablename__ = 'stranka'
    id_stranke    = Column(Integer, primary_key=True)
    ime           = Column(String(100))
    priimek       = Column(String(100), nullable=False)
    mail          = Column(String(100))
    telefon       = Column(String(100))
    id_naj_frizer = Column(Integer, ForeignKey('frizer.id_frizer'), nullable=True)

class Storitev(Base):
    __tablename__ = 'storitev'
    id_storitve  = Column(Integer, primary_key=True)
    ime_storitve = Column(String(100))
    cena         = Column(Numeric(10, 2))
    trajanje     = Column(Time)

class SaloniInStoritve(Base):
    __tablename__ = 'saloni_in_storitve'
    salon_id    = Column(Integer, ForeignKey('salon.id'), primary_key=True)
    storitev_id = Column(Integer, ForeignKey('storitev.id_storitve'), primary_key=True)

class Urnik(Base):
    __tablename__ = 'urnik'
    id_frizerja = Column(Integer, ForeignKey('frizer.id_frizer'), primary_key=True)
    dan         = Column(Date, primary_key=True)
    ura         = Column(Time)

class Rezervacija(Base):
    __tablename__ = 'rezervacija'
    id_rezervacije = Column(Integer, primary_key=True)
    id_stranke     = Column(Integer, ForeignKey('stranka.id_stranke'))
    id_frizerja    = Column(Integer, ForeignKey('frizer.id_frizer'))
    id_salona      = Column(Integer, ForeignKey('salon.id'), nullable=True)
    id_storitve    = Column(Integer, ForeignKey('storitev.id_storitve'), nullable=True)

class Uporabnik(Base):
    __tablename__ = 'users'
    id       = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

class Faq(Base):
    __tablename__ = 'faq'
    id_faq     = Column(Integer, primary_key=True)
    vprasanje  = Column(Text, nullable=False)
    odgovor    = Column(Text, nullable=False)
    vrstni_red = Column(Integer, default=0)
    aktiven    = Column(Boolean, default=True)