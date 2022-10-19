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
import json
import os
from datetime import datetime, timezone
import geopandas as gpd
import intake
import matplotlib.pyplot as plt
import xarray as xr
import climag.plot_configs as cplt
from climag.download_data import download_data

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR_BASE = os.path.join("data", "eurocordex")

# %%
os.makedirs(DATA_DIR_BASE, exist_ok=True)

# %%
# Cork Airport met station coords
LON = -8.48611
LAT = 51.84722

# %%
# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_Ireland_ITM")

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
# add additional time ranges for the MOHC datasets
timerange = timerange + [t.replace("1231", "1230") for t in timerange]

# %%
variables = ["evspsblpot", "mrso", "pr", "rsds", "tas"]

# %%
driving_model_id = [
    "CNRM-CERFACS-CNRM-CM5",
    "ICHEC-EC-EARTH",
    "MPI-M-MPI-ESM-LR",
    "MOHC-HadGEM2-ES"
]

# %% [markdown]
# ## Create local catalogue

# %%
dkrz_cat = intake.open_catalog(["https://dkrz.de/s/intake"])

# %%
server = dkrz_cat._entries["dkrz_cordex_disk"]._open_args["esmcol_obj"]

# %%
server

# %%
dkrz_cordex = intake.open_esm_datastore(
    server,
    read_csv_kwargs={"dtype": {"time_min": "string", "time_max": "string"}}
)

# %%
# download JSON catalogue from DKRZ's GitLab
download_data(server=server, dl_dir=DATA_DIR_BASE)

# %%
# keep data for the relevant variables and time ranges
query = dict(
    CORDEX_domain="EUR-11",
    experiment_id=["historical", "rcp45", "rcp85"],
    frequency="day",
    variable_id=variables,
    time_range=timerange,
    model_id="SMHI-RCA4",
    driving_model_id=driving_model_id,
    member=["r1i1p1", "r12i1p1"]
)

# %%
cordex_eur11 = dkrz_cordex.search(**query)

# %%
cordex_eur11

# %%
cordex_eur11.df.shape

# %%
list(cordex_eur11.df)

# %%
cordex_eur11.df.head()

# %%
# drop v1 of MPI-M-MPI-ESM-LR outputs
cordex_eur11_df = cordex_eur11.df.drop(
    cordex_eur11.df[
        (cordex_eur11.df["driving_model_id"] == "MPI-M-MPI-ESM-LR") &
        (cordex_eur11.df["rcm_version_id"] == "v1")
    ].index
)

# %%
# keep only r12i1p1 outputs of ICHEC-EC-EARTH
cordex_eur11_df = cordex_eur11_df.drop(
    cordex_eur11_df[
        (cordex_eur11_df["driving_model_id"] == "ICHEC-EC-EARTH") &
        (cordex_eur11_df["member"] == "r1i1p1")
    ].index
)

# %%
# replace URI to path to downloaded data
cordex_eur11_df["uri"] = (
    DATA_DIR_BASE + os.sep +
    cordex_eur11_df["institute_id"] + os.sep +
    cordex_eur11_df["experiment_id"] + os.sep +
    cordex_eur11_df["variable_id"] + os.sep +
    cordex_eur11_df["uri"].str.split("/").str[-1]
)

cordex_eur11_df["path"] = cordex_eur11_df["uri"]

# %%
cordex_eur11_df.head()

# %%
cordex_eur11_df.shape

# %%
CSV_FILE_PATH = os.path.join(DATA_DIR_BASE, "eurocordex_eur11_catalogue.csv")

# %%
cordex_eur11_df.to_csv(CSV_FILE_PATH, index=False)

# %%
JSON_FILE_PATH = os.path.join(DATA_DIR_BASE, "dkrz_cordex_disk.json")

# %%
# modify the JSON catalogue
with open(JSON_FILE_PATH, encoding="utf-8") as json_file:
    cordex_eur11_cat = json.load(json_file)
    json_file.close()

# %%
GITHUB_CSV_LINK = (
    "https://raw.githubusercontent.com/ClimAg/data/main/eurocordex/"
    "eurocordex_eur11_catalogue.csv"
)

cordex_eur11_cat["catalog_file"] = GITHUB_CSV_LINK

# %%
cordex_eur11_cat["id"] = "eurocordex_eur11"

# %%
cordex_eur11_cat["description"] = (
    "This is an ESM collection for EURO-CORDEX data used in the ClimAg "
    "project. Data has been generated using the DKRZ intake-esm stores. "
    "Data is filtered for the EUR-11 CORDEX domain at the daily timescale, "
    "the historical (1976-2005) and future (rcp45, rcp85) (2041-2070) "
    "experiments, and the following variables: " + ", ".join(variables) +
    ". The SMHI-RCA4 RCM and four GCMs (" + ", ".join(driving_model_id) +
    ") are the models used to generate these data. Last updated: " +
    str(datetime.now(tz=timezone.utc)) + "."
)

# %%
# save the modified JSON file
JSON_FILE_PATH = os.path.join(DATA_DIR_BASE, "eurocordex_eur11_local.json")

# %%
with open(JSON_FILE_PATH, "w", encoding="utf-8") as json_file:
    json.dump(cordex_eur11_cat, json_file, ensure_ascii=False, indent=4)

# %%
# create a copy that reads the CSV file from disk
cordex_eur11_cat["catalog_file"] = CSV_FILE_PATH
JSON_FILE_PATH = os.path.join(
    DATA_DIR_BASE, "eurocordex_eur11_local_disk.json"
)
with open(JSON_FILE_PATH, "w", encoding="utf-8") as json_file:
    json.dump(cordex_eur11_cat, json_file, ensure_ascii=False, indent=4)

# %% [markdown]
# ## Testing the local catalogue

# %%
# JSON_FILE_PATH = (
#     "https://raw.githubusercontent.com/ClimAg/data/main/eurocordex/"
#     "eurocordex_eur11_local.json"
# )
JSON_FILE_PATH = os.path.join(
    DATA_DIR_BASE, "eurocordex_eur11_local_disk.json"
)

# %%
cordex_eur11_cat = intake.open_esm_datastore(JSON_FILE_PATH)

# %%
list(cordex_eur11_cat)

# %%
cordex_eur11_cat

# %%
cordex_eur11_cat.df.shape

# %%
cordex_eur11_cat.df.head()

# %% [markdown]
# ### Read a subset (precipitation)

# %%
# filter data subset
query = dict(
    experiment_id="rcp85",
    variable_id="pr",
    driving_model_id="MPI-M-MPI-ESM-LR",
)

# %%
cordex_eur11_pr = cordex_eur11_cat.search(**query)

# %%
cordex_eur11_pr

# %%
cordex_eur11_pr.df

# %%
pr = cordex_eur11_pr.to_dataset_dict()

# %%
pr = pr.popitem()[1]

# %%
pr

# %%
# read one of the data files to extract CRS info
data_ec = xr.open_dataset(
    cordex_eur11_pr.df["uri"][0], decode_coords="all", chunks=True
)

# %%
pr.rio.write_crs(data_ec.rio.crs, inplace=True)

# %% [markdown]
# ### Time subset

# %%
pr_50 = pr.sel(time="2055-06-21T12:00:00.000000000")

# %%
plot_transform = cplt.rotated_pole_transform(pr_50)
data_var = pr_50["pr"]  # variable name
plot_data = data_var * 60 * 60 * 24  # convert to mm/day
cbar_label = data_var.attrs["long_name"] + " [mm/day]"  # colorbar label

plt.figure(figsize=(20, 10))
ax = plt.axes(projection=plot_transform)

# specify gridline spacing and labels
ax.gridlines(
    draw_labels=True,
    xlocs=range(-180, 180, 10),
    ylocs=range(-90, 90, 5),
    color="lightslategrey",
    linewidth=.5
)

# plot data for the variable
plot_data.plot(
    ax=ax,
    cmap="GnBu",
    transform=plot_transform,
    x="rlon",
    y="rlat",
    cbar_kwargs=dict(label=cbar_label)
)

# add boundaries
ax.coastlines(resolution="50m", color="darkslategrey", linewidth=.5)

ax.set_title(cplt.cordex_plot_title(pr_50))  # set plot title

plt.show()

# %% [markdown]
# ### Point subset

# %%
cds = cplt.rotated_pole_point(data=pr, lon=LON, lat=LAT)

# %%
pr_ca = pr.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
plt.figure(figsize=(12, 4))
plt.plot(
    pr_ca["time"],
    pr_ca["pr"].values[0] * 60 * 60 * 24
)
plt.xlabel(pr_ca["time"].attrs["standard_name"])
plt.ylabel(pr_ca["pr"].attrs["long_name"] + " [mm/day]")
plt.title(cplt.cordex_plot_title(pr_ca, lon=LON, lat=LAT))
plt.tight_layout()
plt.show()

# %% [markdown]
# ### Ireland subset

# %%
# clip to Ireland's boundary
pr_ie = pr_50.rio.clip(ie.buffer(1).to_crs(pr_50.rio.crs))

# %%
plot_transform = cplt.rotated_pole_transform(pr_ie)
data_var = pr_ie["pr"]  # extract variable name
plot_data = data_var * 60 * 60 * 24  # convert to mm/day
cbar_label = data_var.attrs["long_name"] + " [mm/day]"  # colorbar label

plt.figure(figsize=(20, 10))
ax = plt.axes(projection=plot_transform)

# specify gridline spacing and labels
ax.gridlines(
    draw_labels=True,
    xlocs=range(-180, 180, 2),
    ylocs=range(-90, 90, 1),
    color="lightslategrey",
    linewidth=.5
)

# plot data for the variable
plot_data.plot(
    ax=ax,
    cmap="GnBu",
    transform=plot_transform,
    x="rlon",
    y="rlat",
    cbar_kwargs=dict(label=cbar_label)
)

# add boundaries
ax.coastlines(resolution="10m", color="darkslategrey", linewidth=.75)

ax.set_title(cplt.cordex_plot_title(pr_ie))  # set plot title

plt.show()
