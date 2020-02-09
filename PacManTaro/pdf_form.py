from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    jsonify,
    send_file,
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import pandas as pd
import pandas
import folium
import os
import json
import tempfile
import time

import pdfrw
from reportlab.pdfgen import canvas

import itertools as it

from models import User, Activitat

from __init__ import db

pdf_form = Blueprint("pdf_form", __name__)


def create_overlay(
    nom_act: str = "nombre de la actividad",
    desc: str = "descripción",  # max 90 caracteres
    data_ini: str = "fecha de inicio",
    data_fin: str = "fecha de finalización",
    h11: str = "12:00",
    h12: str = "19:00",
    h21: str = "15:00",
    h22: str = "18:00",
    nombre: str = "Joan",
    nif: str = "47182736 N",
    tit: str = "profesor",
):
    """
    Create the data that will be overlayed on top
    of the form that we want to fill
    """
    c = canvas.Canvas("static/pdfs/simple_form_overlay.pdf")

    c.drawString(170, 421, nom_act)
    c.drawString(50, 358, desc)
    c.drawString(176, 311, "X")  # acte obert public
    c.drawString(64, 248, "X")  # act puntual
    c.drawString(424, 252, data_ini)
    c.drawString(424, 236, data_fin)
    c.drawString(450, 210, h11)
    c.drawString(500, 210, h12)
    c.drawString(450, 185, h21)
    c.drawString(500, 185, h22)
    c.drawString(50, 118, nombre)
    c.drawString(400, 118, nif)
    c.drawString(50, 90, tit)

    c.save()


def merge_pdfs(form_pdf, overlay_pdf, output):
    """
    Merge the specified fillable form PDF with the 
    overlay PDF and save the output
    """
    form = pdfrw.PdfReader(form_pdf)
    olay = pdfrw.PdfReader(overlay_pdf)

    for form_page, overlay_page in zip(form.pages, olay.pages):
        merge_obj = pdfrw.PageMerge()
        overlay = merge_obj.add(overlay_page)[0]
        pdfrw.PageMerge(form_page).add(overlay).render()

    writer = pdfrw.PdfWriter()
    writer.write(output, form)


#


@pdf_form.route("/form_test/<int:id_activitat>")
def form_test(id_activitat):
    actividad = Activitat.query.filter_by(id=id_activitat).first()
    user = User.query.filter_by(id=actividad.user_id).first()
    # user = User.query.filter_by()
    print(actividad.json)
    print(user.json)
    create_overlay(
        nom_act=actividad.titol,
        desc=actividad.descripcio_activitat[:90],  # max 90 caracteres
        data_ini=actividad.data,
        data_fin=actividad.data,
        h11="12:00",
        h12="19:00",
        h21="15:00",
        h22="18:00",
        nombre=user.name,
        nif="47182736 N",
        tit="profesor",
    )

    merge_pdfs(
        "static/pdfs/template.pdf",
        "static/pdfs/simple_form_overlay.pdf",
        "static/pdfs/merged_form.pdf",
    )
    # create_overlay()
    # print(id_activitat)

    return send_file("static/pdfs/merged_form.pdf")

