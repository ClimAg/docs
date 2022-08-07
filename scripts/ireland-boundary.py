# %%
# import libraries
import os
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
from src import download_data as dd

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
# configure plot styles
plt.style.use("seaborn-whitegrid")
plt.rcParams["font.family"] = "Source Sans 3"
plt.rcParams["figure.dpi"] = 150
plt.rcParams["axes.grid"] = False
plt.rcParams["text.color"] = "darkslategrey"
plt.rcParams["axes.labelcolor"] = "darkslategrey"
plt.rcParams["xtick.labelcolor"] = "darkslategrey"
plt.rcParams["ytick.labelcolor"] = "darkslategrey"
plt.rcParams["figure.titleweight"] = "semibold"
plt.rcParams["axes.titleweight"] = "semibold"
plt.rcParams["figure.titlesize"] = "13"
plt.rcParams["axes.titlesize"] = "12"
plt.rcParams["axes.labelsize"] = "10"

# %%
# base data download directory
DATA_DIR = os.path.join("data", "boundary")

# %%
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")

# %% [markdown]
# ## Administrative Areas - OSi National Statutory Boundaries - 2019
# 
# <https://data.gov.ie/dataset/administrative-areas-osi-national-statutory-boundaries-2019>

# %%
URL = (
    "https://data-osi.opendata.arcgis.com/datasets/" +
    "d81188d16e804bde81548e982e80c53e_0.geojson"
)
payload = {
    "outSR": {
        "latestWkid": "2157",
        "wkid": "2157"
    }
}
SUB_DIR = os.path.join(DATA_DIR, "admin-osi", "raw")

# %%
dd.download_data(server=URL, ddir=SUB_DIR, params=payload)

# %%
os.listdir(SUB_DIR)

# %%
DATA_FILE = os.path.join(SUB_DIR, "data.geojson")

# %%
osi = gpd.read_file(DATA_FILE)

# %%
osi

# %%
osi.crs

# %%
base = osi.plot(color="navajowhite", figsize=(9, 9))
osi.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

plt.title("Administrative Areas of the Republic of Ireland")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.text(
    -8, 51.275,
    "© Ordnance Survey Ireland"
)

plt.show()

# %%
osi.to_file(GPKG_BOUNDARY, layer="Admin_Areas_ROI_OSi")

# %% [markdown]
# ## OSNI Open Data - Largescale Boundaries - County Boundaries
# 
# <https://www.opendatani.gov.uk/dataset/osni-open-data-largescale-boundaries-county-boundaries1>

# %%
URL = (
    "https://osni-spatialni.opendata.arcgis.com/datasets/spatialni::" +
    "osni-open-data-largescale-boundaries-county-boundaries-.geojson"
)
payload = {
    "outSR": {
        "latestWkid": "29902",
        "wkid": "29900"
    }
}
SUB_DIR = os.path.join(DATA_DIR, "admin-osni", "raw")

# %%
dd.download_data(server=URL, ddir=SUB_DIR, params=payload)

# %%
os.listdir(SUB_DIR)

# %%
DATA_FILE = os.path.join(SUB_DIR, "data.geojson")

# %%
osni = gpd.read_file(DATA_FILE)

# %%
osni

# %%
osni.crs

# %%
base = osni.plot(color="navajowhite", figsize=(9, 9))
osni.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

plt.title("Administrative Areas of Northern Ireland")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.text(
    -6.5, 53.975,
    "© Ordnance Survey Northern Ireland"
)

plt.show()

# %%
osni.to_file(GPKG_BOUNDARY, layer="Admin_Areas_NI_OSNI")

# %% [markdown]
# ## Boundaries

# %%
osi_roi = osi[["geometry"]].copy()

# %%
osi_roi["NAME"] = "Republic of Ireland"

# %%
osi_roi = osi_roi.dissolve(by="NAME")

# %%
osi_roi.reset_index(inplace=True)

# %%
osi_roi

# %%
base = osi_roi.plot(color="navajowhite", figsize=(9, 9))
osi_roi.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

plt.title("Boundary of the Republic of Ireland")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.text(
    -8, 51.275,
    "© Ordnance Survey Ireland"
)

plt.show()

# %%
osni_ni = osni[["geometry"]].copy()

# %%
osni_ni["NAME"] = "Northern Ireland"

# %%
osni_ni = osni_ni.dissolve(by="NAME")

# %%
osni_ni.reset_index(inplace=True)

# %%
osni_ni

# %%
base = osni_ni.plot(color="navajowhite", figsize=(9, 9))
osni_ni.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

plt.title("Boundary of Northern Ireland")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.text(
    -6.5, 53.975,
    "© Ordnance Survey Northern Ireland"
)

plt.show()

# %%
ie = osi_roi.merge(osni_ni, how="outer")

# %%
ie

# %%
base = ie.plot(color="navajowhite", figsize=(9, 9))
ie.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

plt.title("Boundaries of ROI and NI")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.text(
    -8.25, 51.275,
    "© Ordnance Survey Ireland\n© Ordnance Survey Northern Ireland"
)

plt.show()

# %%
ie.to_file(GPKG_BOUNDARY, layer="Boundary_ROI_NI_OS")

# %% [markdown]
# ## Counties - All-Ireland

# %%
osi_counties = osi.dissolve(by="COUNTY")

# %%
osi_counties

# %%
osi_counties = osi_counties[["CONTAE", "PROVINCE", "geometry"]]

# %%
osi_counties.reset_index(inplace=True)

# %%
osi_counties

# %%
osni_counties = osni.rename(columns={"CountyName": "COUNTY"})

# %%
osni_counties = osni_counties[["geometry", "COUNTY"]]

# %%
osni_counties

# %%
# https://en.wikipedia.org/wiki/Counties_of_Ireland
contae = {
    "ANTRIM": "Aontroim",
    "ARMAGH": "Ard Mhacha",
    "DOWN": "An Dún",
    "FERMANAGH": "Fear Manach",
    "LONDONDERRY": "Doire",
    "TYRONE": "Tír Eoghain"
}

# %%
osni_counties["CONTAE"] = osni_counties["COUNTY"].map(contae)

# %%
osni_counties["PROVINCE"] = "Ulster"

# %%
osni_counties

# %%
ie_counties = osi_counties.merge(osni_counties, how="outer")

# %%
ie_counties

# %%
ie_counties.crs

# %%
base = ie_counties.plot(color="navajowhite", figsize=(9, 9))
ie_counties.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

plt.title("Counties of Ireland")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.text(
    -8.25, 51.275,
    "© Ordnance Survey Ireland\n© Ordnance Survey Northern Ireland"
)

plt.show()

# %%
ie_counties.to_file(GPKG_BOUNDARY, layer="Counties_IE_OS")

# %% [markdown]
# ## All-Ireland boundary

# %%
ie = ie_counties[["geometry"]].copy()

# %%
ie["NAME"] = "Ireland"

# %%
ie = ie.dissolve(by="NAME")

# %%
ie.reset_index(inplace=True)

# %%
ie

# %%
base = ie.plot(color="navajowhite", figsize=(9, 9))
ie.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

plt.title("Boundary of Ireland")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.text(
    -8.25, 51.275,
    "© Ordnance Survey Ireland\n© Ordnance Survey Northern Ireland"
)

plt.show()

# %%
ie.to_file(GPKG_BOUNDARY, layer="Boundary_IE_OS")

# %%



