# %% [markdown]
# # ONS Geography

# %%
import os
from datetime import datetime, timezone
from zipfile import ZipFile
import matplotlib.pyplot as plt
import geopandas as gpd
import pooch

# %%
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
        os.path.join(SUB_DIR, f"{FILE_NAME[:-4]}.txt"), "w", encoding="utf-8"
    ) as outfile:
        outfile.write(
            f"Data downloaded on: {datetime.now(tz=timezone.utc)}\n"
            f"Download URL: {URL}"
        )

# %%
ZipFile(DATA_FILE).namelist()

# %%
data = gpd.read_file(f"zip://{DATA_FILE}!WD_DEC_2022_UK_BFC.shp")

# %%
data.head()

# %%
# filter NI data
data = data[data["WD22CD"].str.contains("N")]

# %%
data.head()

# %%
data.crs

# %%
data.to_file(
    os.path.join(SUB_DIR, "ons_geography.gpkg"),
    layer="ni_wards_12_2022_27700"
)

# %%
# reproject to Irish Transverse Mercator
data.to_crs(2157, inplace=True)

# %%
data.crs

# %%
base = data.plot(color="navajowhite", figsize=(9, 9))
data.boundary.plot(ax=base, color="darkslategrey", linewidth=.2)
plt.ticklabel_format(style="scientific", scilimits=[-4, 4])
plt.show()

# %%
data.to_file(
    os.path.join(SUB_DIR, "ons_geography.gpkg"),
    layer="ni_wards_12_2022_2157"
)
