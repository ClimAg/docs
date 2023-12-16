#!/usr/bin/env python
# coding: utf-8

# # intake-esm
#
# - <https://data-infrastructure-services.gitlab-pages.dkrz.de/tutorials-and-use-cases>
# - <https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/>
# - <https://intake-esm.readthedocs.io/>
# - <https://github.com/intake/intake-esm>
# - <https://gallery.pangeo.io/repos/pangeo-data/pangeo-tutorial-gallery/intake.html>
# - <https://intake.readthedocs.io/>

# import libraries
import json
import os
from datetime import datetime, timezone

import geopandas as gpd
import intake
import matplotlib.pyplot as plt
import numpy as np
import pooch

import climag.plot_configs as cplt

print("Last updated:", datetime.now(tz=timezone.utc))

DATA_DIR_BASE = os.path.join("data", "EURO-CORDEX")

os.makedirs(DATA_DIR_BASE, exist_ok=True)

# Cork Airport met station coords
LON = -8.48611
LAT = 51.84722

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries_all.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")

timerange = [
    "19710101-19751231",
    "19760101-19801231",
    "19810101-19851231",
    "19860101-19901231",
    "19910101-19951231",
    "19960101-20001231",
    "20010101-20051231",
    "20360101-20401231",
    "20410101-20451231",
    "20460101-20501231",
    "20510101-20551231",
    "20560101-20601231",
    "20610101-20651231",
    "20660101-20701231",
]

# add additional time ranges for the MOHC datasets, which use a 360-day year
timerange = timerange + [t.replace("1231", "1230") for t in timerange]

variables = ["evspsblpot", "pr", "rsds", "tas"]

driving_model_id = [
    "CNRM-CERFACS-CNRM-CM5",
    "ICHEC-EC-EARTH",
    "MPI-M-MPI-ESM-LR",
    "MOHC-HadGEM2-ES",
]

# ## Create local catalogue

dkrz_cat = intake.open_catalog(["https://dkrz.de/s/intake"])

server = dkrz_cat._entries["dkrz_cordex_disk"]._open_args["esmcol_obj"]

server

dkrz_cordex = intake.open_esm_datastore(
    server,
    read_csv_kwargs={"dtype": {"time_min": "string", "time_max": "string"}},
)

# download data if necessary
FILE_NAME = "dkrz_cordex_disk.json"
KNOWN_HASH = None
if not os.path.isfile(os.path.join(DATA_DIR_BASE, FILE_NAME)):
    pooch.retrieve(
        url=server, known_hash=KNOWN_HASH, fname=FILE_NAME, path=DATA_DIR_BASE
    )

    with open(
        os.path.join(DATA_DIR_BASE, f"{FILE_NAME[:-5]}.txt"),
        "w",
        encoding="utf-8",
    ) as outfile:
        outfile.write(
            f"Data downloaded on: {datetime.now(tz=timezone.utc)}\n"
            f"Download URL: {server}"
        )

# keep data for the relevant variables and time ranges
query = {
    "CORDEX_domain": "EUR-11",
    "experiment_id": ["historical", "rcp45", "rcp85"],
    "frequency": "day",
    "variable_id": variables,
    "time_range": timerange,
    "model_id": "SMHI-RCA4",
    "driving_model_id": driving_model_id,
    "member": ["r1i1p1", "r12i1p1"],
}

cordex_eur11 = dkrz_cordex.search(**query)

cordex_eur11

cordex_eur11.df.shape

list(cordex_eur11.df)

cordex_eur11.df.head()

# drop v1 of MPI-M-MPI-ESM-LR outputs
cordex_eur11_df = cordex_eur11.df.drop(
    cordex_eur11.df[
        (cordex_eur11.df["driving_model_id"] == "MPI-M-MPI-ESM-LR")
        & (cordex_eur11.df["rcm_version_id"] == "v1")
    ].index
)

# keep only r12i1p1 outputs of ICHEC-EC-EARTH
cordex_eur11_df = cordex_eur11_df.drop(
    cordex_eur11_df[
        (cordex_eur11_df["driving_model_id"] == "ICHEC-EC-EARTH")
        & (cordex_eur11_df["member"] == "r1i1p1")
    ].index
)

# extract driving model name, without the institution
cordex_eur11_df["driving_model"] = cordex_eur11_df["driving_model_id"].replace(
    to_replace={
        "CNRM-CERFACS-CNRM-CM5": "CNRM-CM5",
        "ICHEC-EC-EARTH": "EC-EARTH",
        "MOHC-HadGEM2-ES": "HadGEM2-ES",
        "MPI-M-MPI-ESM-LR": "MPI-ESM-LR",
    }
)

# replace URI to path to downloaded data
cordex_eur11_df["uri"] = (
    DATA_DIR_BASE
    + os.sep
    + "RCA4"
    + os.sep
    + cordex_eur11_df["experiment_id"]
    + os.sep
    + cordex_eur11_df["driving_model"]
    + os.sep
    + cordex_eur11_df["uri"].str.split("/").str[-1]
)

cordex_eur11_df["path"] = cordex_eur11_df["uri"]

cordex_eur11_df.head()

cordex_eur11_df.shape

CSV_FILE_PATH = os.path.join(DATA_DIR_BASE, "eurocordex_eur11_catalogue.csv")

cordex_eur11_df.to_csv(CSV_FILE_PATH, index=False)

JSON_FILE_PATH = os.path.join(DATA_DIR_BASE, "dkrz_cordex_disk.json")

# modify the JSON catalogue
with open(JSON_FILE_PATH, encoding="utf-8") as json_file:
    cordex_eur11_cat = json.load(json_file)
    json_file.close()

GITHUB_CSV_LINK = (
    "https://raw.githubusercontent.com/ClimAg/data/main/eurocordex/"
    "eurocordex_eur11_catalogue.csv"
)

cordex_eur11_cat["catalog_file"] = GITHUB_CSV_LINK

cordex_eur11_cat["id"] = "eurocordex_eur11"

cordex_eur11_cat["description"] = (
    "This is an ESM collection for EURO-CORDEX data used in the ClimAg "
    "project. Data has been generated using the DKRZ intake-esm stores. "
    "Data is filtered for the EUR-11 CORDEX domain at the daily frequency, "
    "the historical (1976-2005) and future (rcp45, rcp85) (2041-2070) "
    "experiments, and the following variables: "
    + ", ".join(variables)
    + ". The SMHI-RCA4 RCM and four GCMs ("
    + ", ".join(driving_model_id)
    + ") are the models used to generate these data. Last updated: "
    + str(datetime.now(tz=timezone.utc))
    + "."
)

# save the modified JSON file
JSON_FILE_PATH = os.path.join(DATA_DIR_BASE, "eurocordex_eur11_local.json")

with open(JSON_FILE_PATH, "w", encoding="utf-8") as json_file:
    json.dump(cordex_eur11_cat, json_file, ensure_ascii=False, indent=4)

# create a copy that reads the CSV file from disk
cordex_eur11_cat["catalog_file"] = CSV_FILE_PATH
JSON_FILE_PATH = os.path.join(
    DATA_DIR_BASE, "eurocordex_eur11_local_disk.json"
)
with open(JSON_FILE_PATH, "w", encoding="utf-8") as json_file:
    json.dump(cordex_eur11_cat, json_file, ensure_ascii=False, indent=4)

# ## Testing the local catalogue

# JSON_FILE_PATH = (
#     "https://raw.githubusercontent.com/ClimAg/data/main/eurocordex/"
#     "eurocordex_eur11_local.json"
# )
JSON_FILE_PATH = os.path.join(
    DATA_DIR_BASE, "eurocordex_eur11_local_disk.json"
)

cordex_eur11_cat = intake.open_esm_datastore(JSON_FILE_PATH)

list(cordex_eur11_cat)

cordex_eur11_cat

cordex_eur11_cat.df.shape

cordex_eur11_cat.df.head()

# ### Read a subset (precipitation)

# filter data subset
query = dict(
    experiment_id="rcp85", variable_id="pr", driving_model_id="ICHEC-EC-EARTH"
)

cordex_eur11_pr = cordex_eur11_cat.search(**query)

cordex_eur11_pr

cordex_eur11_pr.df

pr = cordex_eur11_pr.to_dataset_dict()

pr = pr.popitem()[1]

pr

pr.rio.crs

# ### Time subset

pr_50 = pr.sel(time="2055-06-21")

pr_50

plot_transform = cplt.rotated_pole_transform(pr_50)
data_var = pr_50["pr"]  # variable name
plot_data = data_var * 60 * 60 * 24  # convert to mm day⁻¹
cbar_label = data_var.attrs["long_name"] + " [mm day⁻¹]"  # colorbar label

plt.figure(figsize=(20, 10))
ax = plt.axes(projection=plot_transform)

# specify gridline spacing and labels
ax.gridlines(
    draw_labels=True,
    xlocs=range(-180, 180, 10),
    ylocs=range(-90, 90, 5),
    color="lightslategrey",
    linewidth=0.5,
)

# plot data for the variable
plot_data.plot(
    ax=ax,
    cmap="GnBu",
    transform=plot_transform,
    x="rlon",
    y="rlat",
    cbar_kwargs=dict(label=cbar_label),
    levels=15,
    robust=True,
)

# add boundaries
ax.coastlines(resolution="50m", color="darkslategrey", linewidth=0.5)

plt.show()

# ### Point subset

cds = cplt.rotated_pole_point(data=pr, lon=LON, lat=LAT)

pr_ca = pr.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

plt.figure(figsize=(12, 4))
plt.plot(pr_ca["time"], pr_ca["pr"].values[0] * 60 * 60 * 24)
plt.xlabel(pr_ca["time"].attrs["standard_name"])
plt.ylabel(pr_ca["pr"].attrs["long_name"] + " [mm day⁻¹]")
plt.tight_layout()
plt.show()

# ### Ireland subset

# clip to Ireland's boundary
pr_ie = pr_50.rio.clip(ie.buffer(500).to_crs(pr_50.rio.crs))

# find number of grid cells with data
len(pr_ie["pr"].values.flatten()[np.isfinite(pr_ie["pr"].values.flatten())])

plot_transform = cplt.rotated_pole_transform(pr_ie)
data_var = pr_ie["pr"]  # extract variable name
plot_data = data_var * 60 * 60 * 24  # convert to mm day⁻¹
cbar_label = data_var.attrs["long_name"] + " [mm day⁻¹]"  # colorbar label

plt.figure(figsize=(7, 7))
ax = plt.axes(projection=cplt.projection_hiresireland)

# plot data for the variable
plot_data.plot(
    ax=ax,
    cmap=cplt.cmap_mako_r,
    transform=plot_transform,
    x="rlon",
    y="rlat",
    cbar_kwargs=dict(label=cbar_label),
    levels=10,
    robust=True,
)

# add boundaries
ax.coastlines(resolution="10m", color="darkslategrey", linewidth=0.75)

plt.axis("equal")
plt.tight_layout()
plt.xlim(-1.5, 1.33)
plt.ylim(-2.05, 2.05)

ax.gridlines(
    draw_labels=dict(bottom="x", left="y"),
    xlocs=range(-180, 180, 2),
    ylocs=range(-90, 90, 1),
    color="lightslategrey",
    linewidth=0.5,
    x_inline=False,
    y_inline=False,
)

plt.show()
