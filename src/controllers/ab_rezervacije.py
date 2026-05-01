from flask import render_template, request
from models import model_rezervacije

PER_PAGE = 10  # reservations per page


def pregled_rezervacij():
    vse = model_rezervacije.get_vse_rezervacije()

    # pagination
    total = len(vse)
    try:
        page = max(1, int(request.args.get('stran', 1)))
    except ValueError:
        page = 1

    total_pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)
    page = min(page, total_pages)  # clamp to valid range

    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    rezervacije_stran = vse[start:end]

    return render_template(
        "vse_rezervacije.html",
        rezervacije=rezervacije_stran,
        page=page,
        total_pages=total_pages,
        total=total,
        per_page=PER_PAGE
    )