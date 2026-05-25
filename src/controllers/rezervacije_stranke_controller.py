from flask import render_template, session, redirect
from models import model_rezervacije_stranke


def moje_rezervacije():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "stranka":
        return redirect("/")

    user_id = session["user_id"]

    rezervacije = model_rezervacije_stranke.get_rezervacije_uporabnika(user_id)

    return render_template(
        "rezervacije_stranke.html",
        rezervacije=rezervacije
    )
