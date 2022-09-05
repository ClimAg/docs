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
import geopandas as gpd
import intake
import matplotlib.pyplot as plt
# import requests

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR_BASE = os.path.join("data", "eurocordex")

# %%
os.makedirs(DATA_DIR_BASE, exist_ok=True)

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
# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="Boundary_IE_NUTS_ITM")

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

# %% [markdown]
# ## intake catalogue

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
    "evspsblpot", "hurs", "huss", "mrso", "pr", "ps",
    "rlds", "rsds", "rlus", "rsus", "sund",
    "tas", "tasmax", "tasmin"
]

# %% [markdown]
# ## Create local catalogue

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
cordex_eur11

# %%
cordex_eur11.df.shape

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

# %%
cordex_eur11.df.to_csv(CSV_FILE_PATH, index=False)

# %%
# modify the JSON catalogue
with open(JSON_FILE_PATH, encoding="utf-8") as json_file:
    cordex_eur11_cat = json.load(json_file)
    json_file.close()

# %%
GITHUB_CSV_LINK = (
    "https://media.githubusercontent.com/media/ClimAg/data/main/eurocordex/" +
    "eurocordex_eur11_catalogue.csv"
)

cordex_eur11_cat["catalog_file"] = GITHUB_CSV_LINK

# %%
cordex_eur11_cat["id"] = "eurocordex_eur11"

# %%
cordex_eur11_cat["description"] = (
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
#     "https://raw.githubusercontent.com/ClimAg/data/main/eurocordex/" +
#     "eurocordex_eur11_local.json"
# )
JSON_FILE_PATH = os.path.join(
    DATA_DIR_BASE, "eurocordex_eur11_local_disk.json"
)

# %%
cordex_eur11_cat = intake.open_esm_datastore(JSON_FILE_PATH)

# %%
list(cordex_eur11_cat)[0:5]

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
    driving_model_id="NCC-NorESM1-M",
    experiment_id="rcp85",
    member="r1i1p1",
    model_id="DMI-HIRHAM5",
    rcm_version_id="v3",
    variable_id="pr"
)

# %%
cordex_eur11_pr = cordex_eur11_cat.search(**query)

# %%
cordex_eur11_pr

# %%
cordex_eur11_pr.df

# %%
pr = cordex_eur11_pr.to_dataset_dict(
    cdf_kwargs=dict(chunks=True, decode_coords="all")
)

# %%
pr = pr.popitem()[1]

# %%
pr

# %%
cds = rotated_pole_point(pr, lon=LON, lat=LAT)

# %% [markdown]
# ### Time subset

# %%
pr_50 = pr.isel(time=50)

# %%
data_plot(
    pr_50[pr_50.attrs["intake_esm_varname"][0]] * 60 * 60 * 24,
    cmap="Blues",
    cbar_label=(
        pr_50[pr_50.attrs["intake_esm_varname"][0]].attrs["long_name"] +
        " [mm/day]"
    ),
    plot_title=cordex_plot_title(pr_50),
    transform=rotated_pole_transform(pr_50)
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
    pr_ca[pr_50.attrs["intake_esm_varname"][0]].values[0] * 60 * 60 * 24
)
plt.xlabel(pr_ca["time"].attrs["standard_name"])
plt.ylabel(
    pr_ca[pr_50.attrs["intake_esm_varname"][0]].attrs["long_name"] +
    " [mm/day]"
)
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

# %% [markdown]
# ### Ireland subset

# %%
# clip to Ireland's bounding box with a 10 km buffer
pr_ie = pr_50.rio.clip(ie.envelope.buffer(10000).to_crs(pr_50.rio.crs))

# %%
data_plot(
    pr_ie[pr_ie.attrs["intake_esm_varname"][0]]  * 60 * 60 * 24,
    cmap="viridis_r",
    cbar_label=(
        pr_ie[pr_ie.attrs["intake_esm_varname"][0]].attrs["long_name"] +
        " [mm/day]"
    ),
    plot_title=cordex_plot_title(pr_ie),
    transform=rotated_pole_transform(pr_ie),
    border_width=.75,
    border_res="10m",
    grid_xlocs=range(-180, 180, 2),
    grid_ylocs=range(-90, 90, 1)
)

# # Cork Airport marker
# plt.scatter(cds[0], cds[1], s=100, c="darkslategrey", marker="*")

plt.show()

# %% [markdown]
# ### Save subset as an NC file

# %%
# clip to Ireland's bounding box with a 10 km buffer
pr_ie = pr.rio.clip(ie.envelope.buffer(10000).to_crs(pr.rio.crs))

# %%
pr_ie

# %%
FILE_NAME = (
    pr_ie.attrs["intake_esm_dataset_key"] + "." +
    pr_ie.attrs["driving_model_ensemble_member"] + "." +
    pr_ie.attrs["rcm_version_id"] + "." +
    pr_ie.attrs["intake_esm_varname"][0] + ".nc"
)

# %%
pr_ie.to_netcdf(os.path.join(DATA_DIR_BASE, FILE_NAME))
