from flask import Blueprint, render_template, redirect, url_for, request, flash
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



from models import User, Activitat

from __init__ import db

activity = Blueprint('activity', __name__)


@activity.route('/activity_base')
def search_activity_base():
    return render_template('activity_base.html')

@activity.route("/")
@activity.route('/activity')
def search_activity():
    # TODO: DATA PER DEFECTE, LA D'AVUI
    if current_user.is_authenticated:
        print(current_user)
        print(current_user.name)
        print(current_user.email)
        today_date = time.strftime("%Y-%m-%d")
        return render_template('activity.html', today_date=today_date, load_map=False, actiu=True)
    else:
        return redirect(url_for('main.login'))

@login_required
@activity.route('/activity', methods=['POST'])
def search_activity_post():
    print("SUPPOSED CATEGORY")
    print(request.form.get('category'))
    def read(path="static/databases/equipaments_tots.csv"):
        df = (
            pd.read_csv(path, encoding="ISO-8859-1")
                .dropna(how="all", axis=0)
                .rename(str.lower, axis="columns")
                .rename(lambda x: x.replace(" ", "_"), axis="columns")
                .assign(categoria=lambda x: x["categoria"].str.lower())
        )
        # print("HERE:")
        # print(df.head(2))

        return df

    df = read()

    def get_coords_by_category(
            df: pandas.core.frame.DataFrame = read(),
            category: str = "esports",
            as_list: bool = True,
    ):

        category = category.lower()
        # print(df.head(2))
        df = df[df["categoria"] == category]
        df = df[["nom", "lat", "lng"]]
        df["lat"] = df["lat"].str.replace(",", ".")
        df["lng"] = df["lng"].str.replace(",", ".")

        if as_list:
            return [(name, lat, long) for i, name, lat, long in df.itertuples()]

        return df

    def generate_map(category: str = "esport", return_format: str = "html") -> str:
        """Si el parámnetro return_format = 'html' la función devuelve una ruta de archivo que apunta a
        un archivo .html que al renderizarlo aparece el mapa."""
        
        icon_dict = {
            "esports": "static/esports.png",
            "cultura i oci": "static/cultura.png",
            "educació": "static/education.png",
            "casals": "static/casals.png",
        }
        
        if category not in icon_dict.keys():
            category = "esports"

        category = category.lower()
        print("CATEGORY HERE")
        print(category)

        data = get_coords_by_category(category=category)

        m = folium.Map(location=[41.5411904, 2.4345587], zoom_start=14)

        tooltip = "Click para mas información"
        # print(data[:5])
        for (name, lat, long) in data:
            folium.Marker(
                location=[lat, long],
                radius=12,
                popup=f"""<a href="http://www.google.com/maps/place/{lat},{long}" target="_blank" >{name}</a><br><br><form method="POST" action="/add-activity"><input type="hidden" name="nom_ubicacio" value="{name}"><input type="hidden" name="lat" value="{lat}"><input type="hidden" name="lon" value="{long}"><button type="submit" class="btn btn-primary btn-block">Selecciona aquesta ubicació</button></form>""",
                tooltip=tooltip,
                color="#428bca",
                icon=folium.features.CustomIcon(icon_dict[category], icon_size=(25, 25)),
                fill=True,
                fill_color="#428bca",
            ).add_to(m)

        if return_format == "html":
            #temp_dir = tempfile.mkdtemp(prefix="maphtml")
            path = f"static/maps/folium.html"
            m.save(path)
            print(path)

            return path

        elif return_format == "json":
            return m.to_json()

    activity = request.form.get('activity')
    print("HEEERRE")
    print(activity)



    all_activities= Activitat.query.all()
    all_keywords = [element.keywords for element in all_activities]
    all_keywords = all_keywords if len(all_keywords) > 0 else None


    new_activity = Activitat(
        completed=False,
        titol=request.form.get('titol'),
        comentari_adicional=request.form.get('comentari_adicional'),
        descripcio_activitat=request.form.get('descripcio_activitat'),
        categoria=request.form.get('categoria'),
        remuneracio=request.form.get('remuneracio'),
        url_imatge=getImageURL(request.form.get('titol'), corpus_keys=all_keywords),
        rang_persones=request.form.get('rang_persones'),
        data=request.form.get('data'),
        hora="",
        lat="",
        lon="",
        nom_ubicacio="",
        valoracio_mitjana_activitat="",
        extra="",
        keywords=getKeywords(request.form.get('titol'), corpus_keys=all_keywords), #example: walk,beach,tour
    )
    db.session.add(new_activity)
    db.session.commit()


    return render_template('activity.html',
                           actiu=True,
                           load_map=True,
                           titol=request.form.get('titol'),
                           comentari_adicional=request.form.get('comentari_adicional'),
                           descripcio_activitat=request.form.get('descripcio_activitat'),
                           categoria=request.form.get('categoria'),
                           remuneracio=request.form.get('remuneracio'),
                           url_imatge=request.form.get('url_imatge'),
                           rang_persones=request.form.get('rang_persones'),
                           data=request.form.get('data'),
                           activity=generate_map(category=activity, return_format="html"),
                           )


@activity.route('/add-activity', methods=['POST'])
def add_activity():
    last_activity = Activitat.query.filter_by(id=1).first()
    last_activity.completed = True
    last_activity.nom_ubicacio = request.form.get('nom_ubicacio')
    last_activity.lat = request.form.get('lat')
    last_activity.lon = request.form.get('lon')

    db.session.add(last_activity)
    db.session.commit()
    #return "<head><meta http-equiv='refresh' content='2; URL=http://example.com/'></head><p style='text-align: center;'>Ubicació afegida a l'activitat correctament</p>"
    flash("Ubicació " + request.form.get('nom_ubicacio') + " afegida correctament")
    #return redirect(url_for('activity.allact'))
    return "<a href='/login' target='_blank' onClick='openWindowReload(this)'><p style='text-align: center;'>Ubicació afegida a l'activitat correctament<br><br><button type='submit' class='btn btn-primary btn-block'>Consulta totes les activitats</button></a></p><script>\
			function openWindowReload(link) {\
				var href = link.href;\
				window.open(href,'_blank');\
				document.location.reload(true)\
			}\
		</script>"

@activity.route('/allacts', methods=['GET'])
def allact():
    return "<head><meta http-equiv='refresh' content='2; URL=http://example.com/'></head><p style='text-align: center;'>Ubicació afegida a l'activitat correctament</p>"
    #acts = Activitat.query.all()
    #acts = acts if acts else []
    #return render_template("act_list.html", acts=acts)


@activity.route('/full_list')
def full_list():
    all_activities = Activitat.query.all()
    #print(all_activities.url_imatge)
    """
    for element in all_activities:
        print("NEW:")
        print(element.id)
        print(element.url_imatge)
    print("PRINTED")
    """
    return render_template("full_list.html", all_activities=all_activities)