from flask import render_template
import models.model_salon as model_salon


def setup_db():
    success = model_salon.setup_db()
    tables = {
        "salon": success,
        "frizer": success,
        "stranka": success,
        "storitev": success,
        "urnik": success,
        "rezervacija": success
    }
    return render_template("sv_setup.html", tables=tables)
