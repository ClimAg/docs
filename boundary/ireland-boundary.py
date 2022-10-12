# %% [markdown]
# # Boundaries from Ordnance Survey Ireland / Northern Ireland

# %%
# import libraries
import os
from datetime import datetime, timezone
from zipfile import ZipFile
import geopandas as gpd
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from climag.download_data import download_data

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
# base data download directory
DATA_DIR = os.path.join("data", "boundary")

# %%
GPKG_BOUNDARY = os.path.join(DATA_DIR, "boundaries.gpkg")

# %% [markdown]
# ##  Counties - OSi National Statutory Boundaries - 2019
#
# <https://data-osi.opendata.arcgis.com/datasets/osi::counties-osi-national-statutory-boundaries-2019/about>

# %%
SUB_DIR = os.path.join(DATA_DIR, "admin-osi", "raw")

# %%
# download data if necessary
URL = (
    "https://data-osi.opendata.arcgis.com/datasets/"
    "osi::counties-osi-national-statutory-boundaries-2019.zip"
)

payload = {
    "outSR": {
        "latestWkid": "2157",
        "wkid": "2157"
    }
}

download_data(server=URL, dl_dir=SUB_DIR, params=payload)

# %%
os.listdir(SUB_DIR)

# %%
ZIP_FILE = os.path.join(
    SUB_DIR, "Counties_-_OSi_National_Statutory_Boundaries_-_2019.zip"
)

# %%
# list of files/folders in the ZIP archive
ZipFile(ZIP_FILE).namelist()

# %%
osi = gpd.read_file(
    f"zip://{ZIP_FILE}!Counties___OSi_National_Statutory_Boundaries_.shp"
)

# %%
osi

# %%
osi.crs

# %%
base = osi.plot(color="navajowhite", figsize=(9, 9))
osi.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

plt.title("Counties of the Republic of Ireland")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.text(
    -7.75, 51.275,
    "© Ordnance Survey Ireland"
)

plt.show()

# %%
osi.to_file(GPKG_BOUNDARY, layer="OSi_Counties")

# %% [markdown]
# ## OSNI Open Data - Largescale Boundaries - County Boundaries
#
# <https://www.opendatani.gov.uk/dataset/osni-open-data-largescale-boundaries-county-boundaries1>

# %%
SUB_DIR = os.path.join(DATA_DIR, "admin-osni", "raw")

# %%
# download data if necessary
URL = (
    "https://osni-spatialni.opendata.arcgis.com/datasets/spatialni::"
    "osni-open-data-largescale-boundaries-county-boundaries-.zip"
)

payload = {
    "outSR": {
        "latestWkid": "29902",
        "wkid": "29900"
    }
}

download_data(server=URL, dl_dir=SUB_DIR, params=payload)

# %%
os.listdir(SUB_DIR)

# %%
ZIP_FILE = os.path.join(
    SUB_DIR, "OSNI_Open_Data_-_Largescale_Boundaries_-_County_Boundaries_.zip"
)

# %%
# list of files/folders in the ZIP archive
ZipFile(ZIP_FILE).namelist()

# %%
osni = gpd.read_file(
    f"zip://{ZIP_FILE}!OSNI_Open_Data_-_Largescale_Boundaries_-_"
    "County_Boundaries_.shp"
)

# %%
osni

# %%
osni.crs

# %%
# rename Londonderry to Derry
osni.replace("LONDONDERRY", "DERRY", inplace=True)

# %%
base = osni.plot(color="navajowhite", figsize=(9, 9))
osni.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

plt.title("Administrative Areas of Northern Ireland")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.text(
    -6.35, 53.975,
    "© Ordnance Survey Northern Ireland"
)

plt.show()

# %%
osni.to_file(GPKG_BOUNDARY, layer="OSNI_Counties")

# %% [markdown]
# ## County boundaries - Island of Ireland

# %%
osi_counties = osi[["CONTAE", "COUNTY", "PROVINCE", "geometry"]]

# %%
osi_counties

# %%
osni_counties = osni.rename(columns={"CountyName": "COUNTY"})

# %%
osni_counties = osni_counties[["geometry", "COUNTY"]]

# %%
# https://en.wikipedia.org/wiki/Counties_of_Ireland
contae = {
    "ANTRIM": "Aontroim",
    "ARMAGH": "Ard Mhacha",
    "DOWN": "An Dún",
    "FERMANAGH": "Fear Manach",
    "DERRY": "Doire",
    "TYRONE": "Tír Eoghain"
}

# %%
osni_counties["CONTAE"] = osni_counties["COUNTY"].map(contae)

# %%
osni_counties["PROVINCE"] = "Ulster"

# %%
osni_counties

# %%
# reproject to Irish Transverse Mercator
osi_counties = osi_counties.to_crs(2157)

# %%
osni_counties = osni_counties.to_crs(2157)

# %%
# remove overlapping areas in OSi layer
osi_counties = osi_counties.overlay(osni_counties, how="difference")

# %%
# merge county layers
ie_counties = osi_counties.merge(osni_counties, how="outer")

# %%
ie_counties

# %%
# new colour map
# https://stackoverflow.com/a/31052741
# sample the colormaps that you want to use. Use 20 from each so we get 40
# colors in total
colors1 = plt.cm.tab20b(np.linspace(0., 1, 20))
colors2 = plt.cm.tab20c(np.linspace(0, 1, 20))

# combine them and build a new colormap
colors = np.vstack((colors1, colors2))

# %%
# categorical map - labels directly on plot
base = ie_counties.plot(
    cmap=mcolors.ListedColormap(colors),
    figsize=(9, 9), column="COUNTY", alpha=.45
)

ie_counties.boundary.plot(color="white", ax=base, linewidth=.4)

# ie_counties.centroid.plot(ax=base, color="darkslategrey", markersize=5)

map_labels = zip(
    zip(ie_counties.centroid.x, ie_counties.centroid.y),
    ie_counties["COUNTY"]
)
for xy, lab in map_labels:
    base.annotate(
        text=lab, xy=xy, textcoords="data", rotation=10, ha="center"
    )

plt.title("Counties of Ireland")
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.text(
    612500, 502500,
    "© Ordnance Survey Ireland\n© Ordnance Survey Northern Ireland"
)

plt.show()

# %%
ie_counties.crs

# %%
ie_counties.to_file(GPKG_BOUNDARY, layer="OS_IE_Counties_ITM")

# %%
# reproject to EPSG:4326
ie_counties = ie_counties.to_crs(4326)

# %%
ie_counties.to_file(GPKG_BOUNDARY, layer="OS_IE_Counties")
