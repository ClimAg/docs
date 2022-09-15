# %% [markdown]
# # intake-esm
#
# - <https://data-infrastructure-services.gitlab-pages.dkrz.de/tutorials-and-use-cases>
# - <https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/>
# - <https://intake-esm.readthedocs.io/>
# - <https://github.com/intake/intake-esm>
# - <https://gallery.pangeo.io/repos/pangeo-data/pangeo-tutorial-gallery/intake.html>
# - <https://intake.readthedocs.io/>

# %%
# import libraries
import os
from datetime import datetime, timezone
import intake
import matplotlib.pyplot as plt
import xarray as xr

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR_BASE = os.path.join("data", "eurocordex", "DMI")

# %%
os.makedirs(DATA_DIR_BASE, exist_ok=True)

# %%
# load a dataset to extract metadata
FILE_PATH = os.path.join(
    DATA_DIR_BASE,
    "rcp85",
    "mon",
    "pr_EUR-11_NCC-NorESM1-M_rcp85_r1i1p1_" +
    "DMI-HIRHAM5_v3_mon_204101-205012.nc"
)

data_ec = xr.open_dataset(FILE_PATH, decode_coords="all", chunks=True)

# %% [markdown]
# ## DKRZ intake catalogue

# %%
dkrz_cat = intake.open_catalog(["https://dkrz.de/s/intake"])

# %%
dkrz_cordex = dkrz_cat.dkrz_cordex_disk

# %%
timerange = [
    "19760101-19801231",
    "19810101-19851231",
    "19860101-19901231",
    "19910101-19951231",
    "19960101-20001231",
    "20010101-20051231",
    "20410101-20451231",
    "20460101-20501231",
    "20510101-20551231",
    "20560101-20601231",
    "20610101-20651231",
    "20660101-20701231"
]

# %%
variables = [
    "evspsblpot", "mrso", "pr", "rlds", "rlus", "rsds", "rsus", "sund",
    "tas", "tasmax", "tasmin"
]

# %%
list(dkrz_cat)

# %%
print(dkrz_cat._entries)

# %%
# view CORDEX metadata
dkrz_cat._entries["dkrz_cordex_disk"]._open_args

# %%
dkrz_cordex.esmcol_data["description"]

# %%
dkrz_cordex

# %%
dkrz_cordex.df.head()

# %%
dkrz_cordex.esmcol_data["catalog_file"]

# %%
list(dkrz_cordex.df.columns)

# %%
list(dkrz_cordex.df["CORDEX_domain"].unique())

# %%
list(dkrz_cordex.df["institute_id"].unique())

# %%
list(dkrz_cordex.df["driving_model_id"].unique())

# %%
list(dkrz_cordex.df["experiment_id"].unique())

# %%
list(dkrz_cordex.df["member"].unique())

# %%
list(dkrz_cordex.df["model_id"].unique())

# %%
list(dkrz_cordex.df["rcm_version_id"].unique())

# %%
list(dkrz_cordex.df["frequency"].unique())

# %%
list(dkrz_cordex.df["variable_id"].unique())

# %%
list(dkrz_cordex.df["time_range"].unique())

# %%
# filter for EUR-11, historical and rcp85 experiments only, at daily res
query = dict(
    CORDEX_domain="EUR-11",
    driving_model_id="NCC-NorESM1-M",
    experiment_id="rcp85",
    member="r1i1p1",
    model_id="DMI-HIRHAM5",
    rcm_version_id="v3",
    frequency="day",
    variable_id="pr",
    time_range=timerange
)

# %%
cordex_eur11 = dkrz_cordex.search(**query)

# %%
cordex_eur11

# %%
cordex_eur11.df

# %%
# replace URI to path to downloaded data
cordex_eur11.df["uri"] = (
    "data" + os.sep +
    "eurocordex" + os.sep +
    cordex_eur11.df["institute_id"] + os.sep +
    cordex_eur11.df["experiment_id"] + os.sep +
    cordex_eur11.df["frequency"] + os.sep +
    cordex_eur11.df["uri"].str.split("/").str[-1]
)

# %%
cordex_eur11.df

# %%
pr = cordex_eur11.to_dataset_dict(cdf_kwargs=dict(chunks=dict(time=1)))

# %%
pr

# %%
pr = pr.popitem()[1]

# %%
pr

# %%
pr = pr.isel(time=50)

# %%
pr
