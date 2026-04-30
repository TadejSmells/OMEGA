import os
from functools import wraps
from flask import session, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.environ['DBUSER']}:{quote_plus(os.environ['DBPASS'])}"
    f"@{os.environ['DBHOST']}:{os.environ.get('DBPORT', '5432')}"
    f"/{os.environ['DBNAME']}"
)

# Connection pool configured for better performance under load
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,           # keep 5 connections open
    max_overflow=10,       # allow up to 10 extra connections under load
    pool_pre_ping=True,    # test connections before using them (prevents stale connection errors)
    pool_recycle=300,      # recycle connections every 5 minutes
)

Session = sessionmaker(bind=engine)


def get_session():
    """
    Vrne SQLAlchemy sejo za delo z bazo.
    Vedno zapri sejo po uporabi z session.close() v finally bloku.

    Primer uporabe:
        db_session = db.get_session()
        try:
            rows = db_session.query(Frizer).all()
            return rows
        finally:
            db_session.close()
    """
    return Session()


# ── SECURITY DECORATORS ───────────────────────────────────────────────────────

def login_required(f):
    """
    Zaščiti route pred neprijavljenimi uporabniki.
    Uporaba:
        @f_app.route('/zaščitena-stran')
        @login_required
        def zasčitena_stran():
            ...
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """
    Zaščiti route — dostop samo za admine.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        if session.get("role") != "admin":
            return "Nimaš dostopa — potrebna je vloga admin.", 403
        return f(*args, **kwargs)
    return decorated


def frizer_required(f):
    """
    Zaščiti route — dostop samo za frizerje.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        if session.get("role") not in ("frizer", "admin"):
            return "Nimaš dostopa — potrebna je vloga frizer.", 403
        return f(*args, **kwargs)
    return decorated