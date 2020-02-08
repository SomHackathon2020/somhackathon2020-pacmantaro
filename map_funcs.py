#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import pandas

import folium
import os
import json

import tempfile


def read(path="PacManTaro/static/databases/equipaments_tots.csv"):
    df = (
        pd.read_csv(path, encoding="ISO-8859-1")
        .dropna(how="all", axis=0)
        .rename(str.lower, axis="columns")
        .rename(lambda x: x.replace(" ", "_"), axis="columns")
        .assign(categoria=lambda x: x["categoria"].str.lower())
    )

    return df


df = read()


def get_coords_by_category(
    df: pandas.core.frame.DataFrame = df,
    category: str = "esports",
    as_list: bool = True,
):
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

    data = get_coords_by_category(category=category)

    m = folium.Map(location=[41.5411904, 2.4345587], zoom_start=14)

    tooltip = "Click para mas información"

    for (name, lat, long) in data:

        folium.CircleMarker(
            location=[lat, long],
            radius=12,
            popup=name,
            tooltip=tooltip,
            color="#428bca",
            fill=True,
            fill_color="#428bca",
        ).add_to(m)

    if return_format == "html":
        temp_dir = tempfile.mkdtemp(prefix="maphtml")
        path = f"{temp_dir}/folium.html"
        m.save(path)
        print(path)
        return path

    elif return_format == "json":
        return m.to_json()


generate_map(category="esports", return_format="html")
