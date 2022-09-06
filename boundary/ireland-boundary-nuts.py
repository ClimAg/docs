# %% [markdown]
# # NUTS (Nomenclature of territorial units for statistics)
#
# <https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts>

# %%
# import libraries
import os
import zipfile
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
# from src import download_data as dd

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
# configure plot styles
plt.style.use("seaborn-whitegrid")
plt.rcParams["font.family"] = "Source Sans 3"
plt.rcParams["figure.dpi"] = 96
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

# %%
SUB_DIR = os.path.join(DATA_DIR, "nuts-2021", "raw")

# %%
# # download data if necessary
# URL = (
#     "https://gisco-services.ec.europa.eu/distribution/v2/nuts/download/"
#     "ref-nuts-2021-01m.geojson.zip"
# )

# dd.download_data(server=URL, ddir=SUB_DIR)
# print("Last downloaded:", datetime.now(tz=timezone.utc))

# %%
os.listdir(SUB_DIR)

# %%
DATA_FILE = os.path.join(SUB_DIR, "data.zip")

# %%
zipfile.ZipFile(DATA_FILE).namelist()

# %% [markdown]
# ## NUTS2

# %%
nuts = gpd.read_file(
    "zip://" + DATA_FILE + "!NUTS_RG_01M_2021_4326_LEVL_2.geojson"
)

# %%
nuts.head()

# %%
nuts.crs

# %%
nuts = nuts[nuts["CNTR_CODE"].isin(["IE", "UK"])]

# %%
nuts.head()

# %%
nuts_ie = nuts[nuts["CNTR_CODE"].isin(["IE"])]

# %%
nuts_ie

# %%
nuts_ni = nuts[nuts["CNTR_CODE"].isin(["UK"])]
nuts_ni = nuts[nuts["NUTS_NAME"].str.contains("Ireland")]

# %%
nuts_ni

# %%
nuts2 = nuts_ie.merge(nuts_ni, how="outer")

# %%
nuts2

# %%
nuts2.total_bounds.round(2)

# %%
base = nuts2.plot(color="navajowhite", figsize=(9, 9))
nuts2.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

plt.title("NUTS2 Regions of Ireland")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.text(
    -9.5, 51.275,
    "© EuroGeographics for the administrative boundaries"
)

plt.show()

# %%
nuts2.drop(columns="FID", inplace=True)

# %%
nuts2.to_file(GPKG_BOUNDARY, layer="Admin_Areas_IE_NUTS2")

# %% [markdown]
# ## NUTS3

# %%
nuts = gpd.read_file(
    "zip://" + DATA_FILE + "!NUTS_RG_01M_2021_4326_LEVL_3.geojson"
)

# %%
nuts.head()

# %%
nuts.crs

# %%
nuts = nuts[nuts["CNTR_CODE"].isin(["IE", "UK"])]

# %%
nuts.head()

# %%
nuts_ie = nuts[nuts["CNTR_CODE"].isin(["IE"])]

# %%
nuts_ie

# %%
nuts_ni = nuts[nuts["NUTS_ID"].str.contains("UKN0")]

# %%
nuts_ni

# %%
nuts3 = nuts_ie.merge(nuts_ni, how="outer")

# %%
nuts3

# %%
base = nuts3.plot(color="navajowhite", figsize=(9, 9))
nuts3.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

plt.title("NUTS3 Regions of Ireland")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.text(
    -9.5, 51.275,
    "© EuroGeographics for the administrative boundaries"
)

plt.show()

# %%
nuts3.drop(columns="FID", inplace=True)

# %%
nuts3.to_file(GPKG_BOUNDARY, layer="Admin_Areas_IE_NUTS3")

# %% [markdown]
# ## Boundaries

# %%
ie = nuts3.dissolve(by="CNTR_CODE")

# %%
ie = ie[["geometry"]]

# %%
ie.reset_index(inplace=True)

# %%
ie

# %%
base = ie.plot(color="navajowhite", figsize=(9, 9))
ie.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

plt.title("Boundaries of ROI and NI")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.text(
    -9.5, 51.275,
    "© EuroGeographics for the administrative boundaries"
)

plt.show()

# %%
ie.to_file(GPKG_BOUNDARY, layer="Boundary_ROI_NI_NUTS")

# %%
ie["NAME"] = "Ireland"

# %%
ie = ie.dissolve(by="NAME")

# %%
ie.reset_index(inplace=True)

# %%
ie.drop(columns=["CNTR_CODE"], inplace=True)

# %%
ie

# %%
base = ie.plot(color="navajowhite", figsize=(9, 9))
ie.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

plt.title("Boundary of Ireland")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.text(
    -9.5, 51.275,
    "© EuroGeographics for the administrative boundaries"
)

plt.show()

# %%
ie.to_file(GPKG_BOUNDARY, layer="Boundary_IE_NUTS")

# %% [markdown]
# # Boundaries in Irish transverse mercator
#
# EPSG:2157
#
# See <https://www.gov.uk/government/publications/uk-geospatial-data-standards-register/national-geospatial-data-standards-register#standards-for-coordinate-reference-systems>

# %%
ie.to_crs(2157, inplace=True)

# %%
ie

# %%
base = ie.plot(color="navajowhite", figsize=(9, 9))
ie.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

plt.title("Boundary of Ireland")
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.text(
    550000, 505000,
    "EPSG:2157\n© EuroGeographics for the administrative boundaries"
)

plt.show()

# %%
ie.to_file(GPKG_BOUNDARY, layer="Boundary_IE_NUTS_ITM")
