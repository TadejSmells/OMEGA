import sys
import os
import csv
import io
import logging
from flask import Flask, redirect, render_template, request, Response
from db import login_required, admin_required, frizer_required, csrf_protect, generate_csrf_token, check_session_timeout

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import controllers.sv_setup
import controllers.sv_salon
import controllers.index
import controllers.auth
import controllers.rezervacije
import controllers.storitve
import controllers.ab_rezervacije
import controllers.faq
import controllers.saloni_controller

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

f_app = Flask(__name__, template_folder='templates')
f_app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

f_app.jinja_env.globals['csrf_token'] = generate_csrf_token

# ── SESSION TIMEOUT ───────────────────────────────────────────────────────────
@f_app.before_request
def session_timeout():
    result = check_session_timeout()
    if result is not None:
        return result

# ── ERROR HANDLERS ────────────────────────────────────────────────────────────
@f_app.errorhandler(404)
def not_found(e):
    logger.warning(f"404: {e}")
    return render_template('404.html'), 404

@f_app.errorhandler(500)
def server_error(e):
    logger.error(f"500: {e}")
    return render_template('500.html'), 500

@f_app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

# ── INDEX ─────────────────────────────────────────────────────────────────────
@f_app.get('/')
def home():
    return controllers.index.home()

@f_app.get('/zacetna_stran')
def zacetna_stran_alias():
    return controllers.index.home()

@f_app.get('/setup')
def setup():
    return controllers.sv_setup.setup_db()

@f_app.get('/polni_db')
def polni_db():
    return controllers.sv_setup.polni_db()

# ── AUTH ──────────────────────────────────────────────────────────────────────
@f_app.route("/register", methods=["GET", "POST"])
@csrf_protect
def register():
    return controllers.auth.register()

@f_app.route("/login", methods=["GET", "POST"])
@csrf_protect
def login():
    return controllers.auth.login()

@f_app.get('/logout')
def logout():
    return controllers.auth.logout()

@f_app.get('/profil')
def profil():
    return controllers.auth.profil()

# ── ISKANJE ───────────────────────────────────────────────────────────────────
@f_app.get('/iskanje')
def iskanje():
    from models import model_salon
    query = request.args.get('q', '').strip()
    rezultati = model_salon.iskanje(query)
    return render_template('iskanje.html', query=query, rezultati=rezultati)

# ── SALONI ────────────────────────────────────────────────────────────────────
@f_app.route('/saloni', methods=['GET', 'POST'])
def saloni():
    return controllers.saloni_controller.saloni()

@f_app.route('/salon/<int:salon_id>')
def salon_detail(salon_id):
    return controllers.sv_salon.salon_detail(salon_id)

@f_app.route("/saloni_view")
def saloni_view():
    return controllers.sv_salon.saloni_view()

# ── REZERVACIJE ───────────────────────────────────────────────────────────────
@f_app.route('/rezervacije', methods=['GET', 'POST'])
@login_required
@csrf_protect
def rezervacije():
    return controllers.rezervacije.nova_rezervacija()

@f_app.route('/rezervacije/izbrisi/<int:id_rezervacije>', methods=['POST'])
@login_required
@csrf_protect
def rezervacije_izbrisi(id_rezervacije):
    return controllers.rezervacije.izbrisi_rezervacijo(id_rezervacije)

@f_app.get('/vse_rezervacije')
@login_required
def vse_rezervacije():
    return controllers.ab_rezervacije.pregled_rezervacij()

@f_app.get('/rezervacije/izvoz')
@login_required
def rezervacije_izvoz():
    """Export all reservations as a CSV file download."""
    from models import model_rezervacije

    rows = model_rezervacije.get_vse_rezervacije()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Stranka', 'Frizer', 'Salon', 'Storitev', 'Cena', 'Trajanje', 'Datum', 'Ura'])

    for r in rows:
        writer.writerow([
            r[0], r[1] or '', r[2] or '', r[3] or '',
            r[4] or '', r[5] or '', r[6] or '', r[7] or '', r[8] or '',
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=rezervacije.csv'}
    )

@f_app.route('/zgodovina')
@login_required
def zgodovina():
    return controllers.sv_salon.zgodovina()

# ── STORITVE ──────────────────────────────────────────────────────────────────
@f_app.route('/storitve')
def seznam_storitev():
    return controllers.storitve.pridobi_storitve()

# ── OSTALO ────────────────────────────────────────────────────────────────────
@f_app.route('/stranke')
@login_required
def stranke():
    return controllers.sv_salon.seznam_stranke()

@f_app.route('/urnik', methods=['GET', 'POST'])
def urnik():
    return controllers.sv_salon.urnik()

@f_app.route('/faq', methods=['GET', 'POST'])
def faq():
    return controllers.faq.faq()

@f_app.route("/admin")
@admin_required
def admin():
    return controllers.sv_setup.admin()

@f_app.route("/frizer")
@frizer_required
def frizer():
    return controllers.sv_salon.frizer()

@f_app.route("/stranka")
@login_required
def stranka():
    return controllers.storitve.stranka()

@f_app.get('/termini')
def termini():
    return render_template('termini.html')

# ── ROUTI ZA VAŠE FUNKCIJE, DODAJTE TUKAJ ────────────────────────────────────
#@f_app.route('/"tvoja_pot"')
#@login_required
#@csrf_protect
#def "tvoja_pot"():
#    return controllers.ime_controllerja.funkcija()

if __name__ == "__main__":
    f_app.run(host="0.0.0.0", port=5000, debug=True)