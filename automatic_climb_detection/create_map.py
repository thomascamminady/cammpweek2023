import glob
import json
import os
import warnings

import fire
import folium
import pandas as pd
from folium import features

from automatic_climb_detection import logger

warnings.simplefilter(action="ignore", category=FutureWarning)
import vincent  # noqa


def create_map_file(
    input: str, output: str | None = None, m: folium.Map | None = None
) -> folium.Map:
    df = pd.read_csv(input)
    start = [df["latitude"].dropna().iloc[0], df["longitude"].dropna().iloc[0]]
    finish = [df["latitude"].dropna().iloc[-1], df["longitude"].dropna().iloc[-1]]
    if m is None:
        center = [df["latitude"].dropna().mean(), df["longitude"].dropna().mean()]
        m = folium.Map(location=center, zoom_start=10, tiles="Stamen Terrain")

    coordinates = list(zip(df["latitude"], df["longitude"]))  # noqa
    folium.PolyLine(coordinates).add_to(m)

    start_marker = features.Marker(start, popup=f"Start {os.path.basename(input)}")
    popup = folium.Popup(f"Start {os.path.basename(input)}")
    chart = json.loads(
        vincent.Line(df["altitude"], width=800, height=400)
        .axis_titles(
            x=f"Distance [m] (Stage {os.path.basename(input)})", y="Altitude [m]"
        )
        .to_json()
    )
    vega = features.Vega(chart, height=500, width=1000)
    start_marker.add_child(popup)
    popup.add_child(vega)
    m.add_child(start_marker)

    folium.Marker(
        location=finish,
        popup=f"Finish {os.path.basename(input)}",
        icon=folium.Icon(color="black"),
    ).add_to(m)
    return m


def create_map(input: str, output: str | None = None):
    if os.path.isfile(input):
        m = create_map_file(input, output)
        if output is None:
            output = os.path.splitext(input)[0] + ".html"
            m.save(output)
    elif os.path.isdir(input) and output is None:
        m = folium.Map(
            location=[48.8828, 2.22365], zoom_start=6, tiles="Stamen Terrain"
        )
        csv_files = glob.glob(os.path.join(input, "*.csv"))
        for csv_file in csv_files:
            create_map_file(input=csv_file, m=m)
        m.save(os.path.join(input, "overview.html"))
    else:
        logger.warning("Did not provide filename or foldername.")


if __name__ == "__main__":
    fire.Fire(create_map)
