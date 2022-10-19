# %% [markdown]
# # Irish soil information system
#
# <http://gis.teagasc.ie/soils/index.php>

# %%
import json
from datetime import datetime, timezone
from zipfile import BadZipFile, ZipFile
import geopandas as gpd
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from climag.download_data import download_data

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR = os.path.join("data", "soil")

# %%
os.makedirs(DATA_DIR, exist_ok=True)

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
# new colour map
# https://stackoverflow.com/a/31052741
# sample the colormaps that you want to use. Use 20 from each so we get 40
# colors in total
colors1 = plt.cm.tab20b(np.linspace(0., 1, 20))
colors2 = plt.cm.tab20c(np.linspace(0, 1, 20))

# combine them and build a new colormap
colors = np.vstack((colors1, colors2))

# %%
soil_map.plot(
    column="Associat_S",
    figsize=(9, 9),
    cmap=mcolors.ListedColormap(colors)
)
plt.show()

# %%



