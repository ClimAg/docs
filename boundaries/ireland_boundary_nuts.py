# %% [markdown]
# # NUTS (Nomenclature of territorial units for statistics)
#
# <https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts>

# %%
# import libraries
import os
from datetime import datetime, timezone
from zipfile import BadZipFile, ZipFile
import geopandas as gpd
import matplotlib.pyplot as plt
import pooch
from matplotlib import ticker
import climag.plot_configs as cplt

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
# base data download directory
DATA_DRIVE = "data"
SUB_DIR = os.path.join(DATA_DRIVE, "boundaries", "NUTS2021")
os.makedirs(SUB_DIR, exist_ok=True)

URL = (
    "https://gisco-services.ec.europa.eu/distribution/v2/nuts/download/"
    "ref-nuts-2021-01m.shp.zip"
)
KNOWN_HASH = None
FILE_NAME = "ref-nuts-2021-01m.shp.zip"

# file name for the GeoPackage where the boundary vector layers will be saved
GPKG_BOUNDARY = os.path.join(SUB_DIR, "NUTS_2021.gpkg")

DATA_DIR_TEMP = os.path.join(SUB_DIR, "temp")

os.makedirs(DATA_DIR_TEMP, exist_ok=True)

# %%
# download data if necessary
if not os.path.isfile(os.path.join(SUB_DIR, FILE_NAME)):
    pooch.retrieve(
        url=URL,
        known_hash=KNOWN_HASH,
        fname=FILE_NAME,
        path=SUB_DIR
    )

    with open(
        os.path.join(SUB_DIR, f"{FILE_NAME[:-8]}.txt"), "w", encoding="utf-8"
    ) as outfile:
        outfile.write(
            f"Data downloaded on: {datetime.now(tz=timezone.utc)}\n"
            f"Download URL: {URL}"
        )

# %%
DATA_FILE = os.path.join(SUB_DIR, "ref-nuts-2021-01m.shp.zip")

# %%
ZipFile(DATA_FILE).namelist()

# %%
# extract the archive
try:
    z = ZipFile(DATA_FILE)
    z.extractall(DATA_DIR_TEMP)
except BadZipFile:
    print("There were issues with the file", DATA_FILE)

# %% [markdown]
# ## NUTS0

# %%
DATA_FILE = os.path.join(DATA_DIR_TEMP, "NUTS_RG_01M_2021_4326_LEVL_0.shp.zip")

# %%
ZipFile(DATA_FILE).namelist()

# %%
nuts0 = gpd.read_file(f"zip://{DATA_FILE}!NUTS_RG_01M_2021_4326_LEVL_0.shp")

# %%
nuts0.head()

# %%
nuts0.crs

# %%
# filter for Ireland and UK
nuts0 = nuts0[nuts0["CNTR_CODE"].isin(["IE", "UK"])]

# %%
nuts0

# %%
base = nuts0.plot(color="navajowhite", figsize=(7.5, 7.5))
nuts0.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)
plt.tick_params(labelbottom=False, labelleft=False)

plt.title("NUTS0 Regions of Ireland and UK")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
plt.text(
    -8.75, 49.5,
    "© EuroGeographics for the administrative boundaries"
)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## NUTS1

# %%
DATA_FILE = os.path.join(DATA_DIR_TEMP, "NUTS_RG_01M_2021_4326_LEVL_1.shp.zip")

# %%
nuts1 = gpd.read_file(f"zip://{DATA_FILE}!NUTS_RG_01M_2021_4326_LEVL_1.shp")

# %%
nuts1.head()

# %%
# filter for Ireland and UK
nuts1 = nuts1[nuts1["CNTR_CODE"].isin(["IE", "UK"])]

# %%
nuts1

# %%
# filter for Ireland and Northern Ireland
nuts1 = nuts1[nuts1["NUTS_ID"].isin(["IE0", "UKN"])]

# %%
nuts1

# %%
base = nuts1.plot(color="navajowhite", figsize=(7.5, 7.5))
nuts1.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

base.xaxis.set_major_formatter(cplt.longitude_tick_format)
base.yaxis.set_major_formatter(cplt.latitude_tick_format)
base.yaxis.set_major_locator(ticker.MultipleLocator(1))

plt.title("NUTS1 Regions of Ireland")
plt.text(
    -8.75, 51.275,
    "© EuroGeographics for the administrative boundaries"
)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## NUTS2

# %%
DATA_FILE = os.path.join(DATA_DIR_TEMP, "NUTS_RG_01M_2021_4326_LEVL_2.shp.zip")

# %%
nuts2 = gpd.read_file(f"zip://{DATA_FILE}!NUTS_RG_01M_2021_4326_LEVL_2.shp")

# %%
nuts2.head()

# %%
nuts2 = nuts2[nuts2["NUTS_ID"].str.contains("IE|UKN")]

# %%
nuts2

# %%
nuts2.total_bounds.round(2)

# %%
base = nuts2.plot(color="navajowhite", figsize=(7.5, 7.5))
nuts2.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

base.xaxis.set_major_formatter(cplt.longitude_tick_format)
base.yaxis.set_major_formatter(cplt.latitude_tick_format)
base.yaxis.set_major_locator(ticker.MultipleLocator(1))

plt.title("NUTS2 Regions of Ireland")
plt.text(
    -8.75, 51.275,
    "© EuroGeographics for the administrative boundaries"
)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## NUTS3

# %%
DATA_FILE = os.path.join(DATA_DIR_TEMP, "NUTS_RG_01M_2021_4326_LEVL_3.shp.zip")

# %%
nuts3 = gpd.read_file(f"zip://{DATA_FILE}!NUTS_RG_01M_2021_4326_LEVL_3.shp")

# %%
nuts3.head()

# %%
nuts3 = nuts3[nuts3["NUTS_ID"].str.contains("IE|UKN")]

# %%
nuts3

# %%
base = nuts3.plot(color="navajowhite", figsize=(7.5, 7.5))
nuts3.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

base.xaxis.set_major_formatter(cplt.longitude_tick_format)
base.yaxis.set_major_formatter(cplt.latitude_tick_format)
base.yaxis.set_major_locator(ticker.MultipleLocator(1))

plt.title("NUTS3 Regions of Ireland")
plt.text(
    -8.75, 51.275,
    "© EuroGeographics for the administrative boundaries"
)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Island of Ireland boundary

# %%
ie = nuts1.copy()

# %%
ie = ie.dissolve(by="LEVL_CODE", as_index=False)

# %%
ie

# %%
ie = ie[["geometry"]]

# %%
ie = ie.assign(NAME="Ireland")

# %%
DESCRIPTION = (
    "Boundary for the Island of Ireland generated using NUTS 2021 Level 1 "
    "boundaries"
)

ie = ie.assign(DESCRIPTION=DESCRIPTION)

# %%
ie

# %%
base = ie.plot(color="navajowhite", figsize=(7.5, 7.5))
ie.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

base.xaxis.set_major_formatter(cplt.longitude_tick_format)
base.yaxis.set_major_formatter(cplt.latitude_tick_format)
base.yaxis.set_major_locator(ticker.MultipleLocator(1))

plt.title("Boundary of the Island of Ireland")
plt.text(
    -8.75, 51.275,
    "© EuroGeographics for the administrative boundaries"
)
plt.tight_layout()
plt.show()

# %%
ie.to_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_4326_IE")

# %% [markdown]
# ## Island of Ireland in Irish transverse mercator
#
# Useful for plotting
#
# EPSG:2157
#
# See <https://www.gov.uk/government/publications/uk-geospatial-data-standards-register/national-geospatial-data-standards-register#standards-for-coordinate-reference-systems>

# %%
ie.to_crs(2157, inplace=True)

# %%
ie

# %%
base = ie.plot(color="navajowhite", figsize=(7.5, 7.5))
ie.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)

# plt.ticklabel_format(style="scientific", scilimits=[-4, 4])
# base.xaxis.set_major_locator(ticker.MultipleLocator(1e5))
plt.tick_params(labelbottom=False, labelleft=False)

plt.title("Boundary of Ireland")
# plt.xlabel("Easting (m)")
# plt.ylabel("Northing (m)")
plt.text(
    550000, 505000,
    str(ie.crs).upper() +
    "\n© EuroGeographics for the administrative boundaries"
)
plt.tight_layout()
plt.show()

# %%
ie.to_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")
