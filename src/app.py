import sys
import os
from flask import Flask

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import controllers.sv_setup
import controllers.sv_salon
import controllers.index
import controllers.auth
import controllers.rezervacije          # ← new

f_app = Flask(__name__, template_folder='templates')


@f_app.get('/')
def home():
    return controllers.index.home()


@f_app.get('/setup')
def setup():
    return controllers.sv_setup.setup_db()

@f_app.get('/polni_db')
def polni_db():
    return controllers.sv_setup.polni_db()


@f_app.route('/salon')
def salon_pregled():
    return controllers.sv_salon.pregled()


@f_app.route('/salon/dodaj', methods=['GET', 'POST'])
def salon_dodaj():
    return controllers.sv_salon.dodaj_osebe()


# ── OLD route kept for backwards-compat, redirects to /rezervacije ──────────
@f_app.route('/salon/rezerviraj', methods=['GET', 'POST'])
def salon_rezerviraj_old():
    from flask import redirect
    return redirect('/rezervacije')


@f_app.route('/saloni', methods=['GET', 'POST'])
def saloni():
    return controllers.sv_salon.saloni()


@f_app.route('/storitve', methods=['GET', 'POST'])
def storitve():
    return controllers.sv_salon.storitve()


@f_app.route('/urnik', methods=['GET', 'POST'])
def urnik():
    return controllers.sv_salon.urnik()


# ── RESERVATIONS ─────────────────────────────────────────────────────────────
@f_app.route('/rezervacije', methods=['GET', 'POST'])
def rezervacije():
    return controllers.rezervacije.nova_rezervacija()


@f_app.route('/rezervacije/izbrisi/<int:id_rezervacije>', methods=['POST'])
def rezervacije_izbrisi(id_rezervacije):
    return controllers.rezervacije.izbrisi_rezervacijo(id_rezervacije)


# ── AUTH ──────────────────────────────────────────────────────────────────────
@f_app.route("/register", methods=["GET", "POST"])
def register():
    return controllers.auth.register()

@f_app.route("/login", methods=["GET", "POST"])
def login():
    return controllers.auth.login()


if __name__ == "__main__":
    f_app.run(host="0.0.0.0", port=5000, debug=True)

@app.route("/saloni_view")
def saloni_view():
    return sv_salon.saloni_view()