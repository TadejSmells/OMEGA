import sys
import os
from flask import Flask

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import controllers.sv_setup
import controllers.sv_salon
import controllers.index
import controllers.auth
import controllers.rezervacije      
import controllers.storitve    # ← new

f_app = Flask(__name__, template_folder='templates')


#───────────────────────začetni routi, PUSTI PRI MIRU────────────────────────────
@f_app.get('/')
def home():
    return controllers.index.home()

@f_app.get('/setup')
def setup():
    return controllers.sv_setup.setup_db()

@f_app.get('/polni_db')
def polni_db():
    return controllers.sv_setup.polni_db()
#───────────────────────začetni routi, PUSTI PRI MIRU────────────────────────────


# ─────────────────────────────────AUTH───────────────────────────────────────
@f_app.route("/register", methods=["GET", "POST"])
def register():
    return controllers.auth.register()

@f_app.route("/login", methods=["GET", "POST"])
def login():
    return controllers.auth.login()
# ─────────────────────────────────AUTH───────────────────────────────────────


# ── OLD route kept for backwards-compat, redirects to /rezervacije ──────────
@f_app.route('/salon/rezerviraj', methods=['GET', 'POST'])
def salon_rezerviraj_old():
    from flask import redirect
    return redirect('/rezervacije')


@f_app.route('/saloni', methods=['GET', 'POST'])
def saloni():
    return controllers.sv_salon.saloni()

# ── RESERVATIONS ─────────────────────────────────────────────────────────────
@f_app.route('/rezervacije', methods=['GET', 'POST'])
def rezervacije():
    return controllers.rezervacije.nova_rezervacija()


@f_app.route('/rezervacije/izbrisi/<int:id_rezervacije>', methods=['POST'])
def rezervacije_izbrisi(id_rezervacije):
    return controllers.rezervacije.izbrisi_rezervacijo(id_rezervacije)

@f_app.route("/saloni_view")
def saloni_view():
    return controllers.sv_salon.saloni_view()

#──────────────ROUTI ZA VAŠE FUNKCIJE, DODAJTE TUKAJ────────────────────────────
@f_app.route('/salon')
def salon_pregled():
    return controllers.sv_salon.pregled()

@f_app.route('/stranke')
def stranke():
    return controllers.sv_salon.seznam_stranke()

@f_app.route('/cenik')
def cenik():
    return controllers.storitve.pridobi_storitve()









# ─────────────────────────────────KAR JE SPODAJ PUSTI PRI MIRU───────────────────────────────────────
if __name__ == "__main__":
    f_app.run(host="0.0.0.0", port=5000, debug=True)

