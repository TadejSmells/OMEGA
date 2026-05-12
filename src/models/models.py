from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, Time, Text, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Salon(Base):
    __tablename__ = 'salon'
    id      = Column(Integer, primary_key=True)
    ime     = Column(String(100), nullable=False)
    naslov  = Column(Text)
    mesto   = Column(String(100))
    telefon = Column(String(100))


class Uporabnik(Base):
    __tablename__ = 'users'
    id       = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    vloga    = Column(String(50), default='stranka')


class Frizer(Base):
    __tablename__ = 'frizer'
    id_frizer = Column(Integer, primary_key=True)
    salon_id  = Column(Integer, ForeignKey('salon.id'), nullable=True)
    ime       = Column(String(100))
    kontakt   = Column(String(100))
    user_id   = Column(Integer, ForeignKey('users.id'), nullable=True)


class Stranka(Base):
    __tablename__ = 'stranka'
    id_stranke    = Column(Integer, primary_key=True)
    ime           = Column(String(100))
    priimek       = Column(String(100), nullable=False)
    mail          = Column(String(100))
    telefon       = Column(String(100))
    id_naj_frizer = Column(Integer, ForeignKey('frizer.id_frizer'), nullable=True)
    user_id       = Column(Integer, ForeignKey('users.id'), nullable=True)


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
    datum          = Column(Date)
    ura            = Column(Time)
    status         = Column(String(20), default='active', nullable=False)


class BlokiranTermin(Base):
    __tablename__ = 'blokiran_termin'
    id          = Column(Integer, primary_key=True)
    id_frizerja = Column(Integer, ForeignKey('frizer.id_frizer'), nullable=False)
    datum       = Column(Date, nullable=False)
    ura_od      = Column(Time, nullable=False)
    ura_do      = Column(Time, nullable=False)
    razlog      = Column(String(200))


class Faq(Base):
    __tablename__ = 'faq'
    id_faq     = Column(Integer, primary_key=True)
    vprasanje  = Column(Text, nullable=False)
    odgovor    = Column(Text, nullable=False)
    vrstni_red = Column(Integer, default=0)
    aktiven    = Column(Boolean, default=True)


# ── KOMENTARJI ────────────────────────────────────────────────────────────────

class KomentarSalona(Base):
    __tablename__ = 'komentar_salona'
    id_komentar = Column(Integer, primary_key=True)
    id_salona   = Column(Integer, ForeignKey('salon.id'))
    id_stranke  = Column(Integer, ForeignKey('stranka.id_stranke'))
    ocena       = Column(Integer)           # 1–5, enforced by DB CHECK
    komentar    = Column(Text)
    datum       = Column(DateTime, server_default=func.now())


class KomentarFrizerja(Base):
    __tablename__ = 'komentar_frizerja'
    id_komentar = Column(Integer, primary_key=True)
    id_frizerja = Column(Integer, ForeignKey('frizer.id_frizer'))
    id_stranke  = Column(Integer, ForeignKey('stranka.id_stranke'))
    ocena       = Column(Integer)           # 1–5, enforced by DB CHECK
    komentar    = Column(Text)
    datum       = Column(DateTime, server_default=func.now())


class KomentarStoritve(Base):
    __tablename__ = 'komentar_storitve'
    id_komentar = Column(Integer, primary_key=True)
    id_storitve = Column(Integer, ForeignKey('storitev.id_storitve'))
    id_stranke  = Column(Integer, ForeignKey('stranka.id_stranke'))
    ocena       = Column(Integer)           # 1–5, enforced by DB CHECK
    komentar    = Column(Text)
    datum       = Column(DateTime, server_default=func.now())


# ── SPOROČILA ─────────────────────────────────────────────────────────────────

class Sporocilo(Base):
    """Direktno sporočilo med stranko in frizer jem."""
    __tablename__ = 'sporocilo'
    id          = Column(Integer, primary_key=True)
    id_stranke  = Column(Integer, ForeignKey('stranka.id_stranke'))
    id_frizerja = Column(Integer, ForeignKey('frizer.id_frizer'))
    vsebina     = Column(Text, nullable=False)
    datum       = Column(DateTime, server_default=func.now())
    prebrano    = Column(Boolean, default=False)


class KontaktSporocilo(Base):
    """Kontaktni obrazec — ne veže se na stranko/frizerja."""
    __tablename__ = 'sporocila'
    id       = Column(Integer, primary_key=True)
    ime      = Column(String(100), nullable=False)
    email    = Column(String(120), nullable=False)
    naslov   = Column(String(200), nullable=False)
    vsebina  = Column(Text, nullable=False)
    datum    = Column(DateTime, server_default=func.now())
    prebrano = Column(Boolean, default=False)


# ── PRILJUBLJENI ──────────────────────────────────────────────────────────────

class PriljubljeniFrizerji(Base):
    __tablename__ = 'priljubljeni_frizerji'
    id          = Column(Integer, primary_key=True)
    id_stranke  = Column(Integer, ForeignKey('stranka.id_stranke'))
    id_frizerja = Column(Integer, ForeignKey('frizer.id_frizer'))


class PriljubljeneStoritve(Base):
    __tablename__ = 'priljubljene_storitve'
    id          = Column(Integer, primary_key=True)
    id_stranke  = Column(Integer, ForeignKey('stranka.id_stranke'))
    id_storitve = Column(Integer, ForeignKey('storitev.id_storitve'))


class PriljubljeniSaloni(Base):
    __tablename__ = 'priljubljeni_saloni'
    id         = Column(Integer, primary_key=True)
    id_stranke = Column(Integer, ForeignKey('stranka.id_stranke'))
    id_salona  = Column(Integer, ForeignKey('salon.id'))