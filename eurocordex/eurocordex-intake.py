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
import cartopy.crs as ccrs
import intake
import matplotlib.pyplot as plt
import pandas as pd
import requests
import xarray as xr

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR_BASE = os.path.join("data", "eurocordex")

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

# %%
# convert lat/lon to rotated pole coordinates
def rotated_pole_point(data, lon, lat):
    pole_latitude = (
        data.rio.crs.to_dict(
            projjson=True
        )["conversion"]["parameters"][0]["value"]
    )
    pole_longitude = (
        data.rio.crs.to_dict(
            projjson=True
        )["conversion"]["parameters"][1]["value"]
    )
    rp_cds = ccrs.RotatedGeodetic(
        pole_latitude=pole_latitude, pole_longitude=pole_longitude,
    ).transform_point(x=lon, y=lat, src_crs=ccrs.Geodetic())
    return rp_cds[0], rp_cds[1]

# %%
# Cork Airport met station coords
LON = -8.48611
LAT = 51.84722

# %%
cds = rotated_pole_point(data_ec, lon=LON, lat=LAT)

# %% [markdown]
# ## Plot configurations

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
cordex_eur11

# %%
dkrz_cat = intake.open_catalog(["https://dkrz.de/s/intake"])

# %%
dkrz_cordex = dkrz_cat.dkrz_cordex_disk

# %% [markdown]
# ## intake catalogue

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
    "evspsblpot", "hurs", "huss", "mrso", "pr", "ps",
    "rlds", "rsds", "rlus", "rsus", "sund",
    "tas", "tasmax", "tasmin"
]

# %% [markdown]
# ## Create local catalogue

# %%



# %% [markdown]
# ## intake functionality

# %%
JSON_FILE_PATH = os.path.join(DATA_DIR_BASE, "dkrz_cordex_disk.json")

# %%
# # download JSON catalogue from DKRZ's GitLab
# r = requests.get(
#     dkrz_cat._entries["dkrz_cordex_disk"]._open_args["esmcol_obj"],
#     stream=True
# )

# if r.status_code == 200:
#     with open(JSON_FILE_PATH, "wb") as catfile:
#         for chunk in r.iter_content(chunk_size=1048676):
#             catfile.write(chunk)

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
cordex_eur11.df.to_csv(CSV_FILE_PATH, index=False)

# %%
# modify the JSON catalogue
json_file = open(JSON_FILE_PATH)
eurocordex_eur11 = json.load(json_file)
json_file.close()

# %%
GITHUB_CSV_LINK = (
    "https://media.githubusercontent.com/media/ClimAg/data/main/eurocordex/" +
    "eurocordex_eur11_catalogue.csv?token=AHOG4CXFUAWFBZDPQEOBTOTDCUOD6"
)

eurocordex_eur11["catalog_file"] = GITHUB_CSV_LINK

# %%
eurocordex_eur11["id"] = "eurocordex_eur11"

# %%
eurocordex_eur11["description"] = (
    "This is an ESM collection for EURO-CORDEX data accessible on GitHub " +
    "LFS. Data has been generated using the DKRZ intake-esm stores. " +
    "Data is filtered for the EUR-11 CORDEX domain at the daily timescale, " +
    "the 'historical' (1976-2005) and 'rcp85' (2041-2070) experiments, and " +
    "the following variables: 'evspsblpot', 'hurs', 'huss', 'mrso', 'pr', " +
    "'ps', 'rlds', 'rsds', 'rlus', 'rsus', 'sund', 'tas', 'tasmax', 'tasmin'"
)

# %%
# save the modified JSON file
JSON_FILE_PATH = os.path.join(DATA_DIR_BASE, "eurocordex_eur11_local.json")

# %%
with open(JSON_FILE_PATH, "w", encoding="utf-8") as json_file:
    json.dump(eurocordex_eur11, json_file, ensure_ascii=False, indent=4)

# %% [markdown]
# ## Testing the local catalogue

# %%
GITHUB_JSON_LINK = (
    "https://raw.githubusercontent.com/ClimAg/data/main/eurocordex/" +
    "eurocordex_eur11_local.json?" +
    "token=GHSAT0AAAAAABX3KZBG4HW6U5NNDL7PXT4UYYVDIFQ"
)

local_cat = intake.open_esm_datastore(GITHUB_JSON_LINK)

# %%
list(local_cat)[0:5]

# %%
local_cat

# %%
local_cat.df.shape

# %%
local_cat.df.head()

# %%
# filter data subset
query = dict(
    driving_model_id="NCC-NorESM1-M",
    experiment_id="rcp85",
    member="r1i1p1",
    model_id="DMI-HIRHAM5",
    rcm_version_id="v3",
    variable_id="pr"
)

# %%
cordex_eur11_pr = local_cat.search(**query)

# %%
cordex_eur11_pr

# %%
cordex_eur11_pr.df

# %%
pr = cordex_eur11_pr.to_dataset_dict(cdf_kwargs=dict(chunks=dict(time=1)))

# %%
pr = pr.popitem()[1]

# %%
pr

# %% [markdown]
# ### Time subset

# %%
pr_50 = pr.isel(time=50)

# %%
data_plot(
    pr_50[list(pr_50.keys())[0]] * 60 * 60 * 24,
    cmap="Blues",
    cbar_label=pr_50[list(pr_50.keys())[0]].attrs["long_name"] + " [mm/day]",
    plot_title=cordex_plot_title(pr_50),
    transform=rotated_pole_transform(data_ec)
)
plt.show()

# %% [markdown]
# ### Point subset

# %%
pr_ca = pr.sel({"rlat": cds[1], "rlon": cds[0]}, method="nearest")

# %%
plt.figure(figsize=(12, 4))
plt.plot(
    pr_ca["time"],
    pr_ca[list(pr_ca.keys())[0]].values[0] * 60 * 60 * 24
)
plt.xlabel(pr_ca["time"].attrs["standard_name"])
plt.ylabel(pr_ca[list(pr_ca.keys())[0]].attrs["long_name"] + " [mm/day]")
plt.title(
    pr_ca.attrs["project_id"] + ", " +
    pr_ca.attrs["CORDEX_domain"] + ", " +
    pr_ca.attrs["driving_model_id"] + ", " +
    pr_ca.attrs["driving_model_ensemble_member"] + ", " +
    pr_ca.attrs["driving_experiment_name"] + ", " +
    pr_ca.attrs["model_id"] + ", " +
    pr_ca.attrs["rcm_version_id"] + ", " +
    pr_ca.attrs["frequency"] +
    ", (" + str(LON) + ", " + str(LAT) + ")"
)
plt.tight_layout()
plt.show()

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
    cordex_eur11.df["experiment_id"] + os.sep +
    "day" + os.sep +
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
def data_plot(
    data,
    cmap="terrain",
    vmin=None,
    vmax=None,
    grid_color="lightslategrey",
    border_color="darkslategrey",
    border_width=.5,
    border_res="50m",
    cbar_label=None,
    transform=None,
    grid_xlocs=range(-180, 180, 10),
    grid_ylocs=range(-90, 90, 5),
    plot_title=None,
    plot_figsize=(20, 10)
):
    plt.figure(figsize=plot_figsize)
    ax = plt.axes(projection=transform)
    ax.gridlines(
        draw_labels=True,
        linewidth=.5,
        color=grid_color,
        xlocs=grid_xlocs,
        ylocs=grid_ylocs
    )
    data.plot(
        ax=ax,
        cmap=cmap,
        transform=transform,
        vmin=vmin,
        vmax=vmax,
        x="rlon",
        y="rlat",
        cbar_kwargs={"label": cbar_label}
    )
    ax.coastlines(
        resolution=border_res, color=border_color, linewidth=border_width
    )
    if plot_title is not None:
        ax.set_title(plot_title)

# %% [markdown]
# 

# %%
def cordex_plot_title(data):
    if data.attrs["frequency"] == "mon":
        date_format = "%b %Y"
    elif data.attrs["frequency"] == "day":
        date_format = "%-d %b %Y"
    else:
        date_format = "%Y-%m-%d %H:%M:%S"
    plot_title = (
        data.attrs["project_id"] + ", " +
        data.attrs["CORDEX_domain"] + ", " +
        data.attrs["driving_model_id"] + ", " +
        data.attrs["driving_model_ensemble_member"] + ", " +
        data.attrs["driving_experiment_name"] + ", " +
        data.attrs["model_id"] + ", " +
        data.attrs["rcm_version_id"] + ", " +
        data.attrs["frequency"] + ", " +
        datetime.strftime(
            datetime.fromisoformat(str(data["time"].values)), date_format
        )
    )
    return plot_title

# %%
def rotated_pole_transform(data):
    pole_latitude = (
        data.rio.crs.to_dict(
            projjson=True
        )["conversion"]["parameters"][0]["value"]
    )
    pole_longitude = (
        data.rio.crs.to_dict(
            projjson=True
        )["conversion"]["parameters"][1]["value"]
    )
    transform = ccrs.RotatedPole(
        pole_latitude=pole_latitude, pole_longitude=pole_longitude
    )
    return transform

# %%
FILE_PATH = os.path.join(
    DATA_DIR_BASE,
    "rcp85",
    "mon",
    "pr_EUR-11_NCC-NorESM1-M_rcp85_r1i1p1_" +
    "DMI-HIRHAM5_v3_mon_204101-205012.nc"
)

data_ec = xr.open_dataset(FILE_PATH, decode_coords="all", chunks=True)

# %%
data_plot(
    pr[list(pr.keys())[0]] * 60 * 60 * 24,
    cmap="Blues",
    cbar_label=pr[list(pr.keys())[0]].attrs["long_name"] + " [mm/day]",
    plot_title=cordex_plot_title(pr),
    transform=rotated_pole_transform(data_ec)
)
plt.show()

# %%
# # r = requests.get(dkrz_cordex.esmcol_data["catalog_file"], stream=True)
# # CSV_FILE_PATH = os.path.join(DATA_DIR_BASE, "dkrz_cordex_disk.csv.gz")
# # if r.status_code == 200:
# #     with open(CSV_FILE_PATH, "wb") as catfile:
# #         for chunk in r.iter_content(chunk_size=1048676):
# #             catfile.write(chunk)

# %%
# # dkrz_cordex_data = pd.read_csv(CSV_FILE_PATH, low_memory=False)

# %%
# filter for EUR-11, historical and rcp85 experiments only, at daily res
# keep data for the relevant variables and time ranges
query = dict(
    CORDEX_domain="EUR-11",
    experiment_id=["historical", "rcp85"],
    frequency="day",
    variable_id=variables,
    time_range=timerange
)

# %%
cordex_eur11 = dkrz_cordex.search(**query)

# %%
# replace URI to path to downloaded data
cordex_eur11.df["uri"] = (
    DATA_DIR_BASE + os.sep +
    cordex_eur11.df["experiment_id"] + os.sep +
    "day" + os.sep +
    cordex_eur11.df["uri"].str.split("/").str[-1]
)

# %%
cordex_eur11.df

# %%
CSV_FILE_PATH = os.path.join(DATA_DIR_BASE, "eurocordex_eur11_catalogue.csv")
