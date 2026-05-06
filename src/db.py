import os
import secrets
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

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)


def get_session():
    return Session()


def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']


def validate_csrf():
    from flask import request, abort
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        if not token or token != session.get('csrf_token'):
            abort(403)


# ── SECURITY DECORATORS ───────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        if session.get("role") != "admin":
            return "Nimaš dostopa — potrebna je vloga admin.", 403
        return f(*args, **kwargs)
    return decorated


def frizer_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        if session.get("role") not in ("frizer", "admin"):
            return "Nimaš dostopa — potrebna je vloga frizer.", 403
        return f(*args, **kwargs)
    return decorated