#!/usr/bin/env python
# coding: utf-8

# # Natural Earth 10 m land polygon
#
# <https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-land/>

# import libraries
import os
from datetime import datetime, timezone
from zipfile import BadZipFile, ZipFile

import geopandas as gpd
import matplotlib.pyplot as plt
import pooch
from matplotlib import ticker

import climag.plot_configs as cplt

print("Last updated:", datetime.now(tz=timezone.utc))

# base data download directory
SUB_DIR = os.path.join("data", "boundaries", "NaturalEarth")
os.makedirs(SUB_DIR, exist_ok=True)

URL = "https://naciscdn.org/naturalearth/10m/physical/ne_10m_land.zip"
KNOWN_HASH = None
FILE_NAME = "ne_10m_land.zip"

# file name for the GeoPackage where the boundary vector layers will be saved
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries.gpkg")

DATA_DIR_TEMP = os.path.join(SUB_DIR, "temp")

os.makedirs(DATA_DIR_TEMP, exist_ok=True)

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

DATA_FILE = os.path.join(SUB_DIR, FILE_NAME)

ZipFile(DATA_FILE).namelist()

data = gpd.read_file(f"zip://{DATA_FILE}!ne_10m_land.shp")

data.head()

data.crs

data.plot(figsize=(8, 8), color="seagreen")
plt.tick_params(labelbottom=False, labelleft=False)
plt.show()

# crop Ireland's boundary
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")

data_cropped = data.clip(ie.buffer(12500).to_crs(4326))

data_cropped

# dissolve features
data_cropped["name"] = "Ireland"

data_cropped = data_cropped.dissolve(by="name", as_index=False)

data_cropped.plot(
    figsize=(8, 8),
    color="navajowhite",
    edgecolor="darkslategrey",
    linewidth=0.5,
)
plt.tick_params(labelbottom=False, labelleft=False)
plt.show()

data_cropped.to_file(GPKG_BOUNDARY, layer="ne_10m_land_4326_IE")

# Irish Transverse Mercator
data_cropped.to_crs(2157, inplace=True)

data_cropped

data_cropped.to_file(GPKG_BOUNDARY, layer="ne_10m_land_2157_IE")

# bounding box
ie_bound = gpd.GeoDataFrame(geometry=data_cropped.envelope.buffer(100000))

ie_bound

base = ie_bound.boundary.plot(color="crimson", figsize=(7.5, 7.5))
data_cropped.boundary.plot(ax=base, color="darkslategrey", linewidth=0.4)

plt.tick_params(labelbottom=False, labelleft=False)

plt.title("Boundary of Ireland")
plt.tight_layout()
plt.show()

ie_bound.to_file(GPKG_BOUNDARY, layer="ne_10m_land_2157_IE_BBOX")

# difference between bbox and land polygon
ie_bound = ie_bound.overlay(data_cropped, how="difference")

ie_bound

base = ie_bound.plot(
    color="navajowhite",
    figsize=(7.5, 7.5),
    edgecolor="darkslategrey",
    linewidth=0.4,
)

plt.tick_params(labelbottom=False, labelleft=False)

plt.title("Boundary of Ireland")
plt.tight_layout()
plt.show()

ie_bound.to_file(GPKG_BOUNDARY, layer="ne_10m_land_2157_IE_BBOX_DIFF")
