# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os


DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DBUSER')}:{os.getenv('DBPASS')}"
    f"@{os.getenv('DBHOST', 'localhost')}:{os.getenv('DBPORT', '5432')}"
    f"/{os.getenv('DBNAME')}"
)

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()