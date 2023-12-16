#!/usr/bin/env python
# coding: utf-8

# # Northern Ireland electoral wards
#
# Downloaded from ONS Geography

import os
from datetime import datetime, timezone
from zipfile import ZipFile

import geopandas as gpd
import matplotlib.pyplot as plt
import pooch

import climag.plot_configs as cplt

FILE_NAME = "wards-uk-12-2022.zip"
URL = (
    "https://opendata.arcgis.com/api/v3/datasets/"
    "a2c204fedefe4120ac93f062c647bdcb_0/downloads/data?"
    "format=shp&spatialRefId=27700&where=1%3D1"
)
KNOWN_HASH = None
SUB_DIR = os.path.join("data", "boundaries", "ONS")
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

data = gpd.read_file(f"zip://{DATA_FILE}!WD_DEC_2022_UK_BFC.shp")

data.head()

# filter NI data
data = data[data["WD22CD"].str.contains("N")]

data.head()

data.crs

# reproject to Irish Transverse Mercator
data.to_crs(cplt.ITM_EPSG, inplace=True)

data.crs

base = data.plot(color="navajowhite", figsize=(7, 7))
data.boundary.plot(ax=base, color="darkslategrey", linewidth=0.2)
plt.tick_params(labelbottom=False, labelleft=False)
plt.tight_layout()
plt.show()

data.to_file(
    os.path.join("data", "boundaries", "boundaries_all.gpkg"),
    layer="ONS_NI_wards_12_2022_2157",
)
