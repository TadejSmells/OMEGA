from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()


#zacetek pretovrbe v SQLAlchemy modele
class Salon(Base):
    __tablename__ = 'salon'
    id_salona = Column(Integer, primary_key=True)
    ime       = Column(String(100))
    naslov    = Column(String(200))
    mesto     = Column(String(100))
    telefon   = Column(String(50))

class Frizer(Base):
    __tablename__ = 'frizer'
    id_frizer = Column(Integer, primary_key=True)
    salon_id  = Column(Integer, ForeignKey('salon.id_salona'), nullable=True)
    ime       = Column(String(100))
    kontakt   = Column(String(50))

class Stranka(Base):
    __tablename__ = 'stranka'
    id_stranke    = Column(Integer, primary_key=True)
    ime           = Column(String(100))
    priimek       = Column(String(100))
    mail          = Column(String(150))
    telefon       = Column(String(50))
    id_naj_frizer = Column(Integer, ForeignKey('frizer.id_frizer'), nullable=True)

class Storitev(Base):
    __tablename__ = 'storitev'
    id_storitve = Column(Integer, primary_key=True)
    ime         = Column(String(100))
    cena        = Column(Numeric(8, 2))
    trajanje    = Column(Integer)  # minutes

class Urnik(Base):
    __tablename__ = 'urnik'
    id_urnik    = Column(Integer, primary_key=True)
    id_frizerja = Column(Integer, ForeignKey('frizer.id_frizer'))
    dan         = Column(String(20))
    ura         = Column(String(10))

class Rezervacija(Base):
    __tablename__ = 'rezervacija'
    id_rezervacije = Column(Integer, primary_key=True)
    id_stranke     = Column(Integer, ForeignKey('stranka.id_stranke'))
    id_frizerja    = Column(Integer, ForeignKey('frizer.id_frizer'))
    salon_id       = Column(Integer, ForeignKey('salon.id_salona'), nullable=True)
    storitev_id    = Column(Integer, ForeignKey('storitev.id_storitve'), nullable=True)