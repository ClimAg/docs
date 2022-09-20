# %% [markdown]
# # Boundaries from Ordnance Survey Ireland / Northern Ireland

# %%
# import libraries
import os
from datetime import datetime, timezone
from zipfile import ZipFile
import climag.plot_configs
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
osi.to_file(GPKG_BOUNDARY, layer="Admin_Areas_ROI_OSi")

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
    -7.75, 51.275,
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
    -6.35, 53.975,
    "© Ordnance Survey Northern Ireland"
)

plt.show()

# %%
ie = osi_roi.merge(osni_ni, how="outer")

# %%
ie

# %%
ie.total_bounds.round(2)

# %%
base = ie.plot(color="navajowhite", figsize=(9, 9))
ie.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

plt.title("Boundaries of ROI and NI")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.text(
    -7.75, 51.275,
    "© Ordnance Survey Ireland\n© Ordnance Survey Northern Ireland"
)

plt.show()

# %%
ie.to_file(GPKG_BOUNDARY, layer="Boundary_ROI_NI_OS")

# %% [markdown]
# ## Counties - Island of Ireland

# %%
osi

# %%
osi_counties = osi[["CONTAE", "COUNTY", "PROVINCE", "geometry"]]

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
    -7.75, 51.275,
    "© Ordnance Survey Ireland\n© Ordnance Survey Northern Ireland"
)

plt.show()

# %%
ie_counties.to_file(GPKG_BOUNDARY, layer="Counties_IE_OS")

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
ie_counties_itm = ie_counties.to_crs(2157)  # convert CRS to ITM

base = ie_counties_itm.plot(
    cmap=mcolors.ListedColormap(colors),
    figsize=(9, 9), column="COUNTY", alpha=.45
)

ie_counties_itm.boundary.plot(color="white", ax=base, linewidth=.4)

# ie_counties_itm.centroid.plot(ax=base, color="darkslategrey", markersize=5)

map_labels = zip(
    zip(ie_counties_itm.centroid.x, ie_counties_itm.centroid.y),
    ie_counties_itm["COUNTY"]
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
ie_counties_itm.to_file(GPKG_BOUNDARY, layer="Counties_IE_OS_ITM")

# %% [markdown]
# ## Island of Ireland boundary

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
    -7.75, 51.275,
    "© Ordnance Survey Ireland\n© Ordnance Survey Northern Ireland"
)

plt.show()

# %%
ie.to_file(GPKG_BOUNDARY, layer="Boundary_IE_OS")
