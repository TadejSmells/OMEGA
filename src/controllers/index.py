from flask import request, render_template
from models.models import Stranka
from db import get_session


def get_all_stranke():
    session = get_session()
    return session.query(Stranka).all()


def home():
    return render_template("index.html", stranke=get_all_stranke())


def stranke():
    return render_template("stranke.html", stranke=get_all_stranke())