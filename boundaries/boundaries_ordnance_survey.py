#!/usr/bin/env python
# coding: utf-8

# # Ireland county boundaries

import os
from datetime import datetime, timezone
from zipfile import ZipFile

import geopandas as gpd
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pooch
from matplotlib import ticker

import climag.climag as cplt

# base data download directory
DATA_DIR = os.path.join("data", "boundaries")

GPKG_BOUNDARY = os.path.join(DATA_DIR, "boundaries_all.gpkg")

# ##  Counties - OSi National Statutory Boundaries - 2019
#
# <https://data-osi.opendata.arcgis.com/datasets/osi::counties-osi-national-statutory-boundaries-2019/about>

SUB_DIR = os.path.join(DATA_DIR, "OSi")
os.makedirs(SUB_DIR, exist_ok=True)
URL = (
    "https://opendata.arcgis.com/api/v3/datasets/"
    "e6f6418eb62442c4adbe18d0a64135a2_0/downloads/data?"
    "format=shp&spatialRefId=2157&where=1%3D1"
)
KNOWN_HASH = None
FILE_NAME = "counties-osi-national-statutory-boundaries-2019.zip"

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

ZIP_FILE = os.path.join(
    SUB_DIR, "counties-osi-national-statutory-boundaries-2019.zip"
)

# list of files/folders in the ZIP archive
ZipFile(ZIP_FILE).namelist()

osi = gpd.read_file(
    f"zip://{ZIP_FILE}!Counties___OSi_National_Statutory_Boundaries_.shp"
)

osi

osi.crs

base = osi.plot(
    color="navajowhite",
    figsize=(9, 9),
    edgecolor="darkslategrey",
    linewidth=0.4,
)

plt.tick_params(labelbottom=False, labelleft=False)
plt.title("Counties of the Republic of Ireland")
plt.text(650000, 505000, "© Ordnance Survey Ireland")

plt.tight_layout()
plt.show()

# ## OSNI Open Data - Largescale Boundaries - County Boundaries
#
# <https://www.opendatani.gov.uk/dataset/osni-open-data-largescale-boundaries-county-boundaries1>

SUB_DIR = os.path.join(DATA_DIR, "OSNI")
os.makedirs(SUB_DIR, exist_ok=True)
URL = (
    "https://osni-spatialni.opendata.arcgis.com/datasets/"
    "spatialni::osni-open-data-largescale-boundaries-county-boundaries-.zip?"
    'outSR={"latestWkid":29902,"wkid":29900}'
)
KNOWN_HASH = None
FILE_NAME = "osni-open-data-largescale-boundaries-county-boundaries.zip"

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

ZIP_FILE = os.path.join(SUB_DIR, FILE_NAME)

# list of files/folders in the ZIP archive
ZipFile(ZIP_FILE).namelist()

osni = gpd.read_file(
    f"zip://{ZIP_FILE}!OSNI_Open_Data_-_Largescale_Boundaries_-_"
    "County_Boundaries_.shp"
)

osni

osni.crs

# rename Londonderry to Derry
osni.replace("LONDONDERRY", "DERRY", inplace=True)

base = osni.plot(
    color="navajowhite",
    figsize=(7.5, 7.5),
    edgecolor="darkslategrey",
    linewidth=0.4,
)

plt.tick_params(labelbottom=False, labelleft=False)
plt.title("Counties of Northern Ireland")
plt.text(312000, 305000, "© Ordnance Survey Northern Ireland")

plt.tight_layout()
plt.show()

# ## County boundaries - Island of Ireland

osi_counties = osi[["CONTAE", "COUNTY", "PROVINCE", "geometry"]]

osi_counties

osni_counties = osni.rename(columns={"CountyName": "COUNTY"})

osni_counties = osni_counties[["geometry", "COUNTY"]]

# https://en.wikipedia.org/wiki/Counties_of_Ireland
contae = {
    "ANTRIM": "Aontroim",
    "ARMAGH": "Ard Mhacha",
    "DOWN": "An Dún",
    "FERMANAGH": "Fear Manach",
    "DERRY": "Doire",
    "TYRONE": "Tír Eoghain",
}

osni_counties["CONTAE"] = osni_counties["COUNTY"].map(contae)

osni_counties["PROVINCE"] = "Ulster"

osni_counties

# reproject to Irish Transverse Mercator
osi_counties = osi_counties.to_crs(cplt.ITM_EPSG)

osni_counties = osni_counties.to_crs(cplt.ITM_EPSG)

# remove overlapping areas in OSi layer
osi_counties = osi_counties.overlay(osni_counties, how="difference")

# merge county layers
ie_counties = osi_counties.merge(osni_counties, how="outer")

ie_counties

# new colour map
# https://stackoverflow.com/a/31052741
# sample the colormaps that you want to use. Use 20 from each so we get 40
# colors in total
colors1 = plt.cm.tab20b(np.linspace(0.0, 1, 20))
colors2 = plt.cm.tab20c(np.linspace(0, 1, 20))

# combine them and build a new colormap
colors = np.vstack((colors1, colors2))

# categorical map - labels directly on plot
base = ie_counties.plot(
    cmap=mcolors.ListedColormap(colors),
    edgecolor="white",
    linewidth=0.4,
    figsize=(9, 9),
    column="COUNTY",
    alpha=0.45,
)

map_labels = zip(
    zip(ie_counties.centroid.x, ie_counties.centroid.y), ie_counties["COUNTY"]
)
for xy, lab in map_labels:
    base.annotate(text=lab, xy=xy, textcoords="data", rotation=10, ha="center")

plt.tick_params(labelbottom=False, labelleft=False)
plt.title("Counties of Ireland")
plt.text(
    612500,
    502500,
    "© Ordnance Survey Ireland\n© Ordnance Survey Northern Ireland",
)

plt.show()

ie_counties.crs

ie_counties.to_file(GPKG_BOUNDARY, layer="OSi_OSNI_IE_Counties_2157")
