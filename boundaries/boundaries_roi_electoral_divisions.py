#!/usr/bin/env python
# coding: utf-8

# # Republic of Ireland electoral divisions

import os
from datetime import datetime, timezone
from zipfile import ZipFile
import matplotlib.pyplot as plt
import geopandas as gpd
import pooch

URL = (
    "https://opendata.arcgis.com/api/v3/datasets/"
    "429c839036934413bb740bea190f2596_0/downloads/data?"
    "format=shp&spatialRefId=2157&where=1%3D1"
)

KNOWN_HASH = None
FILE_NAME = "electoral-divisions-2019.zip"
SUB_DIR = os.path.join("data", "boundaries", "OSi")
DATA_FILE = os.path.join(SUB_DIR, FILE_NAME)
os.makedirs(SUB_DIR, exist_ok=True)

# download data if necessary
if not os.path.isfile(os.path.join(SUB_DIR, FILE_NAME)):
    pooch.retrieve(
        url=URL, known_hash=KNOWN_HASH, fname=FILE_NAME, path=SUB_DIR
    )

    with open(
        os.path.join(SUB_DIR, f"{FILE_NAME[:-4]}.txt"), "w", encoding="utf-8"
    ) as outfile:
        outfile.write(
            f"Data downloaded on: {datetime.now(tz=timezone.utc)}\n"
            f"Download URL: {URL}"
        )

ZipFile(DATA_FILE).namelist()

data = gpd.read_file(
    f"zip://{DATA_FILE}!"
    "Electoral_Divisions_-_OSi_National_Statutory_Boundaries_-_2019.shp"
)

data.head()

data.crs

base = data.plot(color="navajowhite", figsize=(7.5, 7.5))
data.boundary.plot(ax=base, color="darkslategrey", linewidth=0.2)
plt.tick_params(labelbottom=False, labelleft=False)
plt.tight_layout()
plt.show()

data.to_file(
    os.path.join("data", "boundaries", "boundaries_all.gpkg"),
    layer="OSi_IE_electoral_divisions_2019",
)

