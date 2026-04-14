from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import create_engine, String, Text, select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker, Mapped, mapped_column, relationship
from dotenv import load_dotenv
import os

load_dotenv()




DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DBUSER')}:{os.getenv('DBPASS')}"
    f"@{os.getenv('DBHOST', 'localhost')}:{os.getenv('DBPORT', '5432')}"
    f"/{os.getenv('DBNAME')}"
)
print(DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=False)

class Base(DeclarativeBase):
    pass

class Stranka(Base):
    __tablename__ = "stranka"

    id_stranke: Mapped[int] = mapped_column(primary_key=True)
    id_naj_frizer: Mapped[Optional[int]] = mapped_column(ForeignKey("frizer.id_frizer"), nullable=True)
    ime: Mapped[Optional[str]] = mapped_column(String(100))
    priimek: Mapped[str] = mapped_column(String(100), nullable=False)
    mail: Mapped[Optional[str]] = mapped_column(String(100))
    telefon: Mapped[Optional[str]] = mapped_column(String(100))

    def __repr__(self):
        return f"<Stranka(id={self.id_stranke}, ime='{self.ime}', priimek='{self.priimek}')>"
    

class Frizer(Base):
    __tablename__ = "frizer"

    id_frizer: Mapped[int] = mapped_column(primary_key=True)


if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("Connected to DB successfully!")
    except Exception as e:
        print("Connection failed:", e)



Session = sessionmaker(bind=engine)

def get_session():
    return Session()