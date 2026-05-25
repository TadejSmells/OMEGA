from flask import render_template, session, redirect, request, flash
from models import model_cenikstoritev
from models import model_priljubljene_storitve


def pridobi_storitve():
    try:
        podatki = model_cenikstoritev.get_vse_storitve()
    except Exception:
        podatki = []

    priljubljeni_ids = set()
    if session.get("user_id") and session.get("role") == "stranka":
        try:
            priljubljeni_ids = model_priljubljene_storitve.get_priljubljene_ids(
                session["user_id"]
            )
        except Exception:
            priljubljeni_ids = set()

    # Priljubljene storitve naj bodo na začetku seznama (stabilno: ostalo ostane v istem vrstnem redu)
    podatki = sorted(podatki, key=lambda row: 0 if row[0] in priljubljeni_ids else 1)

    return render_template(
        "seznam_storitev.html",
        podatki=podatki,
        priljubljeni_ids=priljubljeni_ids,
    )
    


def dodaj_storitev():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "admin":
        return "Nimaš dostopa.", 403

    if request.method == "POST":
        ime_storitve = request.form.get("ime_storitve", "").strip()
        cena         = request.form.get("cena", "").strip()
        trajanje     = request.form.get("trajanje", "").strip()

        if not ime_storitve or not cena or not trajanje:
            flash("Vsa polja so obvezna.", "error")
            return redirect("/storitve/dodaj")

        try:
            cena = float(cena)
        except ValueError:
            flash("Cena mora biti število.", "error")
            return redirect("/storitve/dodaj")

        try:
            model_cenikstoritev.dodaj_storitev(ime_storitve, cena, trajanje)
            flash(f"Storitev '{ime_storitve}' je bila uspešno dodana.", "success")
            return redirect("/storitve")
        except ValueError as e:
            flash(str(e), "error")
            return redirect("/storitve/dodaj")
        except Exception:
            flash("Napaka pri dodajanju storitve. Poskusi znova.", "error")
            return redirect("/storitve/dodaj")

    return render_template("dodaj_storitev.html")


def stranka():
    if "user_id" not in session:
        return redirect("/login")

    if session["role"] != "stranka":
        return "Nimaš dostopa"

    return "Stranka panel"