# %% [markdown]
# # Irish soil information system
#
# <http://gis.teagasc.ie/soils/index.php>

# %%
import json
import os
from datetime import datetime, timezone
from zipfile import ZipFile
import geopandas as gpd
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from matplotlib import ticker
from climag.download_data import download_data

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR = os.path.join("data", "soil")

# %%
os.makedirs(DATA_DIR, exist_ok=True)

# %%
# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_Ireland_ITM")

# %% [markdown]
# ## Soil associations

# %%
# get full list of soil associations
URL = "http://gis.teagasc.ie/soils/services/get_all_associations.php"
try:
    r = requests.get(URL, stream=True, timeout=3000)
    print("Last downloaded:", datetime.now(tz=timezone.utc))
    soil_associations = pd.DataFrame(r.json())
    soil_associations.to_csv(
        os.path.join(DATA_DIR, "soil_associations.csv"), index=False
    )
except requests.exceptions.RequestException as err:
    print("Data download unsuccessful!", err)

# %%
soil_associations.head()

# %% [markdown]
# ## Soil series

# %%
# get full list of soil series
URL = "http://gis.teagasc.ie/soils/services/get_all_series.php"
try:
    r = requests.get(URL, stream=True, timeout=3000)
    print("Last downloaded:", datetime.now(tz=timezone.utc))
    soil_series = pd.DataFrame(r.json())
    soil_series.to_csv(
        os.path.join(DATA_DIR, "soil_series.csv"), index=False
    )
except requests.exceptions.RequestException as err:
    print("Data download unsuccessful!", err)

# %%
soil_series.head()

# %% [markdown]
# ## Individual soil associations, full details

# %%
# individual soil associations, full details
soil_associations_full = {}
for s in list(soil_associations["Association_Unit"]):
    URL = f"http://gis.teagasc.ie/soils/get_associations.php?assoc_id={s}"
    try:
        r = requests.get(URL, stream=True, timeout=3000)
        print("Last downloaded:", datetime.now(tz=timezone.utc))
        soil_associations_full[s] = r.json()
    except requests.exceptions.RequestException as err:
        print("Data download unsuccessful!", err)

JSON_FILE_PATH = os.path.join(DATA_DIR, "soil_associations_full.json")
with open(JSON_FILE_PATH, "w", encoding="utf-8") as json_file:
    json.dump(soil_associations_full, json_file, ensure_ascii=False, indent=4)

# %%
soil_associations_full_df = pd.DataFrame(soil_associations_full).T

# %%
soil_associations_full_df.head()

# %% [markdown]
# ### Soil associations and series

# %%
JSON_FILE_PATH = os.path.join(DATA_DIR, "soil_associations_full.json")

# %%
with open(JSON_FILE_PATH, encoding="utf-8") as json_file:
    soil_associations_full = json.load(json_file)
    json_file.close()

# %%
soil = {}
for key in soil_associations_full.keys():
    for i in range(len(soil_associations_full[key]['SeriesArray'])):
        val = (
            soil_associations_full[key]['SeriesArray'][i]['National_Series_Id']
        )
        soil[val] = key

# %%
soil_df = pd.DataFrame.from_dict(
    data=soil, orient="index", columns=["soil_association"]
)

# %%
soil_df.index.name = "soil_series"

# %%
soil_df.head()

# %%
soil_df.to_csv(os.path.join(DATA_DIR, "soil_assoc_series.csv"))

# %%
soil_df.shape

# %%
len(soil_df.index.unique())

# %%
len(soil_df["soil_association"].unique())

# %% [markdown]
# ## Individual soil series, full details

# %%
# individual soil series, full details
soil_series_full = {}
for s in list(soil_series["National_Series_Id"]):
    URL = f"http://gis.teagasc.ie/soils/get_series.php?series_id={s}"
    try:
        r = requests.get(URL, stream=True, timeout=3000)
        print("Last downloaded:", datetime.now(tz=timezone.utc))
        soil_series_full[s] = r.json()
    except requests.exceptions.RequestException as err:
        print("Data download unsuccessful!", err)

JSON_FILE_PATH = os.path.join(DATA_DIR, "soil_series_full.json")
with open(JSON_FILE_PATH, "w", encoding="utf-8") as json_file:
    json.dump(soil_series_full, json_file, ensure_ascii=False, indent=4)

# %%
soil_series_full_df = pd.DataFrame(soil_series_full).T

# %%
soil_series_full_df.head()

# %%
soil_series_full_df.to_csv(
    os.path.join(DATA_DIR, "soil_series_full.csv"), index=False
)

# %% [markdown]
# ## Individual soil series, full details plus representative information

# %%
# individual soil series, full details, plus representative site and horizon
# information
soil_series_full_rep = {}
for s in list(soil_series["National_Series_Id"]):
    URL = f"http://gis.teagasc.ie/soils/get_series_full.php?series_code={s}"
    try:
        r = requests.get(URL, stream=True, timeout=3000)
        print("Last downloaded:", datetime.now(tz=timezone.utc))
        soil_series_full_rep[s] = r.json()
    except requests.exceptions.RequestException as err:
        print("Data download unsuccessful!", err)

JSON_FILE_PATH = os.path.join(DATA_DIR, "soil_series_full_rep.json")
with open(JSON_FILE_PATH, "w", encoding="utf-8") as json_file:
    json.dump(soil_series_full_rep, json_file, ensure_ascii=False, indent=4)

# %%
soil_series_full_rep_df = pd.DataFrame(soil_series_full_rep).T

# %%
soil_series_full_rep_df.head()

# %% [markdown]
# ### Nitrogen totals

# %%
JSON_FILE_PATH = os.path.join(DATA_DIR, "soil_series_full_rep.json")

# %%
with open(JSON_FILE_PATH, encoding="utf-8") as json_file:
    soil_series_full_rep = json.load(json_file)
    json_file.close()

# %%
nitrogen = {}
for key in soil_series_full_rep.keys():
    if len(soil_series_full_rep[key]["Horizons"]) > 0:
        val = soil_series_full_rep[key]["Horizons"][0]["Total_Nitrogen"]
        if val is not None:
            nitrogen[key] = val

# %%
nitrogen_df = pd.DataFrame.from_dict(
    data=nitrogen, orient="index", columns=["total_nitrogen"]
)

# %%
nitrogen_df.index.name = "id"

# %%
nitrogen_df.head()

# %%
nitrogen_df.to_csv(os.path.join(DATA_DIR, "soil_nitrogen.csv"))

# %%
nitrogen_df.shape

# %%
len(nitrogen_df.index.unique())

# %% [markdown]
# ### Merge with soil associations/series

# %%
soil_nitrogen = pd.merge(
    nitrogen_df, soil_df, left_index=True, right_index=True
)

# %%
soil_nitrogen.reset_index(inplace=True)

# %%
soil_nitrogen.rename(columns={"index": "soil_series"}, inplace=True)

# %%
soil_nitrogen.shape

# %%
soil_nitrogen.head()

# %% [markdown]
# ## Soil map

# %%
# download data
URL = "http://gis.teagasc.ie/soils/downloads/INSM250k_ING_1b.zip"
download_data(server=URL, dl_dir=DATA_DIR)

# %%
os.listdir(DATA_DIR)

# %%
ZIP_FILE = os.path.join(DATA_DIR, "INSM250k_ING_1b.zip")

# %%
# list of files/folders in the ZIP archive
ZipFile(ZIP_FILE).namelist()

# %%
soil_map = gpd.read_file(f"zip://{ZIP_FILE}!INSM250k_ING.shp")

# %%
soil_map.head()

# %%
soil_map.crs

# %%
soil_map.shape

# %%
soil_map["Associatio"].unique()

# %%
soil_map["Associat_1"].unique()

# %%
soil_map["Associat_S"].unique()

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
base = soil_map.plot(
    column="Associat_S",
    figsize=(9, 9),
    cmap=mcolors.ListedColormap(colors)
)
ie.to_crs(soil_map.crs).boundary.plot(ax=base, color="black", linewidth=1)
base.xaxis.set_major_locator(ticker.MultipleLocator(1e5))
plt.ticklabel_format(style="scientific", scilimits=[-4, 4])
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.text(
    200000, 4000, "EPSG:29902\n"
    "Data: Irish Soil Information System\n"
    "(Teagasc, EPA, Cranfield)"
)
plt.title("Irish soil map")
plt.show()

# %% [markdown]
# ### Merge with soil data

# %%
soil_map_merged = pd.merge(
    soil_nitrogen, soil_map, left_on="soil_association", right_on="Associatio"
)

# %%
soil_map_merged.head()

# %%
soil_map_merged = gpd.GeoDataFrame(soil_map_merged).dissolve(
    by="soil_association"
)

# %%
soil_map_merged.shape

# %%
soil_map_merged.head()

# %%
base = soil_map_merged.plot(
    column="total_nitrogen", cmap="viridis", legend=True, figsize=(9, 9),
    legend_kwds={"label": "Total nitrogen (%)"}
)
ie.to_crs(soil_map_merged.crs).boundary.plot(
    ax=base, color="black", linewidth=1
)
base.xaxis.set_major_locator(ticker.MultipleLocator(1e5))
plt.ticklabel_format(style="scientific", scilimits=[-4, 4])
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.text(
    200000, 4000, "EPSG:29902\n"
    "Data: Irish Soil Information System\n"
    "(Teagasc, EPA, Cranfield)"
)
# plt.title("Irish soil map")
plt.show()

# %%
soil_map_merged.to_file(
    os.path.join(DATA_DIR, "soil.gpkg"), layer="soil_nitrogen"
)
