from flask import request, redirect, session
from db import get_session
from models.models import KomentarFrizerja


def dodaj(frizer_id):
    if "user_id" not in session:
        return redirect("/login")

    ocena = request.form.get("ocena")
    komentar = request.form.get("komentar")

    if not ocena or not komentar:
        return redirect(f"/frizer/{frizer_id}")

    session_db = get_session()

    try:
        nov = KomentarFrizerja(
            id_frizerja=frizer_id,
            id_stranke=session["user_id"],
            ocena=int(ocena),
            komentar=komentar
        )

        session_db.add(nov)
        session_db.commit()

    finally:
        session_db.close()

    return redirect(f"/frizer/{frizer_id}")