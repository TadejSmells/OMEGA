import os
import secrets
import time
from functools import wraps
from flask import session, redirect, request, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.environ['DBUSER']}:{quote_plus(os.environ['DBPASS'])}"
    f"@{os.environ['DBHOST']}:{os.environ.get('DBPORT', '5432')}"
    f"/{os.environ['DBNAME']}"
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
)

Session = sessionmaker(bind=engine)

SESSION_TIMEOUT_SECONDS = 30 * 60  # 30 minutes of inactivity


def get_session():
    """
    Vrne SQLAlchemy sejo za delo z bazo.
    Vedno zapri sejo po uporabi z session.close() v finally bloku.
    """
    return Session()


# ── SESSION TIMEOUT ───────────────────────────────────────────────────────────

def check_session_timeout():
    """
    Called before every request via @f_app.before_request in app.py.
    If the user has been inactive for SESSION_TIMEOUT_SECONDS, clears
    their session and redirects to login.

    Only runs if the user is logged in — anonymous users are unaffected.
    Exempt routes: /login, /logout, /register, /profil, static files.
    """
    # skip if not logged in
    if 'user_id' not in session:
        return

    # skip auth and static routes to avoid redirect loops
    exempt = {'/login', '/logout', '/register', '/profil'}
    if request.path in exempt or request.path.startswith('/static'):
        return

    now = time.time()
    last_active = session.get('last_active', now)

    if now - last_active > SESSION_TIMEOUT_SECONDS:
        session.clear()
        return redirect('/login')

    # update last active timestamp on every request
    session['last_active'] = now
    session.modified = True


# ── CSRF PROTECTION ───────────────────────────────────────────────────────────

def generate_csrf_token():
    """Generira CSRF token in ga shrani v Flask session."""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']


def validate_csrf():
    """Preveri CSRF token pri POST zahtevah."""
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        if not token or token != session.get('csrf_token'):
            abort(403)


def csrf_protect(f):
    """
    Dekorator ki zaščiti route pred CSRF napadi.
    Uporaba:
        @f_app.route('/login', methods=['GET', 'POST'])
        @csrf_protect
        def login():
            ...
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        validate_csrf()
        return f(*args, **kwargs)
    return decorated


# ── SECURITY DECORATORS ───────────────────────────────────────────────────────

def login_required(f):
    """Zaščiti route pred neprijavljenimi uporabniki."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Zaščiti route — dostop samo za admine."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        if session.get("role") != "admin":
            return "Nimaš dostopa — potrebna je vloga admin.", 403
        return f(*args, **kwargs)
    return decorated


def frizer_required(f):
    """Zaščiti route — dostop samo za frizerje in admine."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        if session.get("role") not in ("frizer", "admin"):
            return "Nimaš dostopa — potrebna je vloga frizer.", 403
        return f(*args, **kwargs)
    return decorated