from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import pandas as pd
import pandas
import folium
import os
import json
import tempfile
import time
from img_api_utils import *

import re
import string


from models import User, Activitat

from __init__ import db

acts_map = Blueprint("acts_map", __name__)


def myfloat(x):
    if x != "NULL" and x != "" and x != " ":
        return float(x)
    else:
        print(f"I got a bad float: {x}")
        return None


def clean_str(s):

    s = re.sub(f"[^{re.escape(string.printable)}]", "", s)
    s = s.rstrip().strip()
    s = s.encode().decode()
    print(s)
    print(type(s))
    s = myfloat(s)
    print(f"converted float: {s}")

    return s


@acts_map.route("/acts_map")
def return_current_map():

    events = Activitat.query.all()

    def get_coords_by_category(
        # df: pandas.core.frame.DataFrame = read(),
        # category: str = "esports",
        # as_list: bool = True,
        events=events,
    ):

        # category = category.lower()

        data = [
            (a.titol, clean_str(a.lat), clean_str(a.lon), str(a.categoria).lower())
            for a in events
        ]

        print(data)

        return data

        # print(df.head(2))
        # df = df[df["categoria"] == category]
        # df = df[["nom", "lat", "lng"]]
        # df["lat"] = df["lat"].str.replace(",", ".")
        # df["lng"] = df["lng"].str.replace(",", ".")

        # if as_list:
        #     return [(name, lat, long) for i, name, lat, long in df.itertuples()]

        # return df

    def generate_map():
        """Si el parámnetro return_format = 'html' la función devuelve una ruta de archivo que apunta a
        un archivo .html que al renderizarlo aparece el mapa."""

        icon_dict = {
            "esports": "static/img/esports.png",
            "cultura i oci": "static/img/cultura.png",
            "educació": "static/img/education.png",
            "casals": "static/img/casals.png",
        }

        data = get_coords_by_category()

        m = folium.Map(location=[41.5411904, 2.4345587], zoom_start=14)

        tooltip = "Click para mas información"
        # print(data[:5])
        for (name, lat, long, category) in data:
            if not lat or not long:
                continue
            if category not in icon_dict.keys():
                category = "esports"
            folium.Marker(
                location=[lat, long],
                radius=12,
                popup=f"""<a href="http://www.google.com/maps/place/{lat},{long}" target="_blank" >{name}</a>""",
                tooltip=tooltip,
                color="#428bca",
                icon=folium.features.CustomIcon(
                    icon_dict[category], icon_size=(25, 25)
                ),
                fill=True,
                fill_color="#428bca",
            ).add_to(m)

        # if return_format == "html":
        # temp_dir = tempfile.mkdtemp(prefix="maphtml")
        path = f"/static/maps/folium.html"
        print(f"saving map to: {path}")
        m.save(path)
        print(path)

        return

    generate_map()
    # print(path)

    return render_template("acts_map.html")

