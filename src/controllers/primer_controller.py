# ── PRIMER CONTROLLERJA ───────────────────────────────────────────────────────
# Ta datoteka je VZOREC — pokaže kako mora izgledati controller.
# Kopiraj ta vzorec ko delaš svojo controller datoteko.
#
# KORAKI za nov user story:
# 1. Ustvari src/models/model_ime.py  (podatki iz baze)
# 2. Ustvari src/controllers/ime.py   (logika, ta vzorec)
# 3. Dodaj route v src/app.py
# 4. Ustvari src/templates/ime.html

from flask import render_template
# from models import model_primer_modela  # ← zamenjaj z dejanskim modelom


def funkcija():
    # podatki = model_primer_modela.get_vse_podatke()
    podatki = []  # začasno prazno dokler ni model narejen

    return render_template(
        "primer_template.html",  # ← zamenjaj z dejanskim templateom
        podatki=podatki
    )