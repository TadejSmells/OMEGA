import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.environ['DBUSER']}:{quote_plus(os.environ['DBPASS'])}"
    f"@{os.environ['DBHOST']}:{os.environ.get('DBPORT', '5432')}"
    f"/{os.environ['DBNAME']}"
)

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

def get_session():
    """
    Vrne SQLAlchemy sejo za delo z bazo.
    Vedno zapri sejo po uporabi z session.close() v finally bloku.

    Primer uporabe:
        session = db.get_session()
        try:
            rows = session.query(Frizer).all()
            return rows
        finally:
            session.close()
    """
    return Session()