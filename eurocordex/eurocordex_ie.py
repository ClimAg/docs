#!/usr/bin/env python
# coding: utf-8

# # Subset EURO-CORDEX data for Ireland

# import libraries
import os
import glob
from datetime import datetime, timezone
import geopandas as gpd
import intake
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xarray as xr
from dask.distributed import Client
import climag.plot_configs as cplt

print("Last updated:", datetime.now(tz=timezone.utc))

client = Client(n_workers=2, threads_per_worker=4, memory_limit="3GB")

client

DATA_DIR_BASE = os.path.join("data", "EURO-CORDEX")

# directory to store outputs
DATA_DIR = os.path.join(DATA_DIR_BASE, "IE")
os.makedirs(DATA_DIR, exist_ok=True)

# Moorepark met station coords
LON, LAT = -8.26389, 52.16389

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")
ie_bbox = gpd.read_file(
    GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE_BBOX_DIFF"
)
ie_ne = gpd.read_file(GPKG_BOUNDARY, layer="ne_10m_land_2157_IE_BBOX_DIFF")

# ## Reading the local catalogue

JSON_FILE_PATH = os.path.join(
    DATA_DIR_BASE, "eurocordex_eur11_local_disk.json"
)

cordex_eur11_cat = intake.open_esm_datastore(JSON_FILE_PATH)

list(cordex_eur11_cat)

cordex_eur11_cat

cordex_eur11_cat.df.shape

cordex_eur11_cat.df.head()

# ## Read a subset (historical)

cordex_eur11 = cordex_eur11_cat.search(
    experiment_id="historical", driving_model_id="ICHEC-EC-EARTH"
)

cordex_eur11

cordex_eur11.df

data = xr.open_mfdataset(
    glob.glob(
        "/run/media/nms/MyPassport/EURO-CORDEX/RCA4/historical/EC-EARTH/*.nc"
        # "data/EURO-CORDEX/RCA4/historical/EC-EARTH/*.nc"
    ),
    chunks="auto",
    decode_coords="all",
)

# data = xr.open_mfdataset(
#     list(cordex_eur11.df["uri"]),
#     chunks="auto",
#     decode_coords="all"
# )

data

# using Moorepark met station coordinates
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

# copy CRS
data_crs = data.rio.crs

data_crs

# subset for reference period and spin-up year
data = data.sel(time=slice("1975", "2005"))

# copy time_bnds coordinates
data_time_bnds = data.coords["time_bnds"]

data

# ## Ireland subset

# clip to Ireland's boundary
data = data.rio.clip(ie.buffer(6500).to_crs(data_crs), all_touched=True)

# number of grid cells with data
len(
    data.groupby("time.season")
    .mean(dim="time")["tas"][0]
    .values.flatten()[
        np.isfinite(
            data.groupby("time.season")
            .mean(dim="time")["tas"][0]
            .values.flatten()
        )
    ]
)

cplt.plot_map(
    data=data.groupby("time.season").mean(dim="time").sel(season="JJA"),
    var="tas",
)

cplt.plot_map(
    data=data.groupby("time.season").mean(dim="time").sel(season="JJA"),
    var="tas",
    boundary_data=ie_bbox,
)

cplt.plot_map(
    data=data.groupby("time.season").mean(dim="time").sel(season="JJA"),
    var="tas",
    contour=True,
)

cplt.plot_map(
    data=data.groupby("time.season").mean(dim="time").sel(season="JJA"),
    var="tas",
    contour=True,
    boundary_data=ie_bbox,
)

data

# ## Visualise fields

# ### Monthly averages

for var in data.data_vars:
    cplt.plot_averages(
        data=data.sel(time=slice("1976", "2005")),
        var=var,
        averages="month",
        boundary_data=ie_ne,
        cbar_levels=16,
    )

# ### Time series

data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

data_ie_df = pd.DataFrame({"time": data_ie["time"]})
# configure plot title
plot_title = []
for var in data_ie.data_vars:
    data_ie_df[var] = data_ie[var]
    plot_title.append(
        f"{data_ie[var].attrs['long_name']} [{data_ie[var].attrs['units']}]"
    )

data_ie_df.set_index("time", inplace=True)

data_ie_df.plot(
    subplots=True,
    layout=(4, 1),
    figsize=(12, 11),
    legend=False,
    xlabel="",
    title=plot_title,
    linewidth=0.5,
)

plt.tight_layout()
plt.show()

# ### Box plots

data_ie = data_ie.sel(time=slice("1976", "2005"))

data_ie_df = pd.DataFrame({"time": data_ie["time"]})
for var in data_ie.data_vars:
    data_ie_df[var] = data_ie[var]
data_ie_df.set_index("time", inplace=True)

fig, axs = plt.subplots(2, 2, figsize=(12, 4))
for ax, var in zip(axs.flat, data_ie.data_vars):
    data_ie_df.plot.box(
        column=var,
        vert=False,
        showmeans=True,
        ax=ax,
        patch_artist=True,
        color={
            "medians": "Crimson",
            "whiskers": "DarkSlateGrey",
            "caps": "DarkSlateGrey",
        },
        boxprops={"facecolor": "Lavender", "color": "DarkSlateGrey"},
        meanprops={
            "markeredgecolor": "DarkSlateGrey",
            "marker": "d",
            "markerfacecolor": (1, 1, 0, 0),  # transparent
        },
        flierprops={
            "alpha": 0.5,
            "markeredgecolor": "LightSteelBlue",
            "zorder": 1,
        },
    )
    ax.set_title(
        f"{data_ie[var].attrs['long_name']} [{data_ie[var].attrs['units']}]"
    )
    ax.set(yticklabels=[])
plt.tight_layout()
plt.show()

# ## Calculate photosynthetically active radiation

# Papaioannou et al. (1993) - irradiance ratio
data = data.assign(PAR=data["rsds"] * 0.473)

data

# compare radiation vals
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest").sel(
    time=slice("1997", "1999")
)

data_ie_df = pd.DataFrame({"time": data_ie["time"]})
for var in ["rsds", "PAR"]:
    data_ie_df[var] = data_ie[var]

data_ie_df.set_index("time", inplace=True)

data_ie_df.plot(figsize=(12, 4), xlabel="", colormap="viridis")
plt.tight_layout()
plt.show()

data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest").sel(
    time=slice("1976", "2005")
)

fig = data_ie_df.plot.box(
    vert=False,
    showmeans=True,
    figsize=(10, 3),
    patch_artist=True,
    color={
        "medians": "Crimson",
        "whiskers": "DarkSlateGrey",
        "caps": "DarkSlateGrey",
    },
    boxprops={"facecolor": "Lavender", "color": "DarkSlateGrey"},
    meanprops={
        "markeredgecolor": "DarkSlateGrey",
        "marker": "d",
        "markerfacecolor": (1, 1, 0, 0),  # transparent
    },
    flierprops={
        "alpha": 0.5,
        "markeredgecolor": "LightSteelBlue",
        "zorder": 1,
    },
)
plt.tight_layout()
plt.show()

# ## Convert units and rename variables

for v in data.data_vars:
    var_attrs = data[v].attrs  # extract attributes
    if v == "tas":
        var_attrs["units"] = "°C"
        data[v] = data[v] - 273.15
        var_attrs["note"] = "Converted from K to °C by subtracting 273.15"
    elif v == "PAR":
        var_attrs["units"] = "MJ m⁻² day⁻¹"
        data[v] = data[v] * (60 * 60 * 24 / 1e6)
        var_attrs["long_name"] = "Surface Photosynthetically Active Radiation"
        var_attrs["note"] = (
            "Calculated by multiplying surface downwelling shortwave "
            "radiation with an irradiance ratio of 0.473 based on Papaioannou "
            "et al. (1993); converted from W m⁻² to MJ m⁻² day⁻¹ by "
            "multiplying 0.0864 based on the FAO Irrigation and Drainage "
            "Paper No. 56 (Allen et al., 1998, p. 45)"
        )
    elif v in ("pr", "evspsblpot"):
        var_attrs["units"] = "mm day⁻¹"
        data[v] = data[v] * 60 * 60 * 24
        var_attrs["note"] = (
            "Converted from kg m⁻² s⁻¹ to mm day⁻¹ by multiplying 86,400,"
            " assuming a water density of 1,000 kg m⁻³"
        )
    data[v].attrs = var_attrs  # reassign attributes

# rename variables
data = data.rename({"tas": "T", "pr": "PP", "evspsblpot": "PET"})

# assign dataset name
for x in ["CNRM-CM5", "EC-EARTH", "HadGEM2-ES", "MPI-ESM-LR"]:
    if x in data.attrs["driving_model_id"]:
        data.attrs[
            "dataset"
        ] = f"IE_EURO-CORDEX_RCA4_{x}_{data.attrs['experiment_id']}"

# keep only required variables
data = data.drop_vars(["rsds"])

# assign attributes to the data
data.attrs["comment"] = (
    "This dataset has been clipped with the Island of Ireland's boundary and "
    "units have been converted. "
    "Last updated: "
    + str(datetime.now(tz=timezone.utc))
    + " by nstreethran@ucc.ie."
)

# reassign time_bnds
data.coords["time_bnds"] = data_time_bnds

# reassign CRS
data.rio.write_crs(data_crs, inplace=True)

data.rio.crs

# ## Visualise

# ### Monthly averages

cplt.plot_averages(
    data=data.sel(time=slice("1976", "2005")),
    var="T",
    averages="month",
    boundary_data=ie_ne,
    cbar_levels=[3 + 1 * n for n in range(13)],
)

for var in ["PAR", "PET", "PP"]:
    cplt.plot_averages(
        data=data.sel(time=slice("1976", "2005")),
        var=var,
        averages="month",
        boundary_data=ie_ne,
        cbar_levels=12,
    )

# ### Seasonal averages

for var in data.data_vars:
    cplt.plot_averages(
        data=data.sel(time=slice("1976", "2005")),
        var=var,
        averages="season",
        boundary_data=ie_ne,
        cbar_levels=12,
    )

# ### Time series

data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

data_ie

data_ie_df = pd.DataFrame({"time": data_ie["time"]})
# configure plot title
plot_title = []
for var in data_ie.data_vars:
    data_ie_df[var] = data_ie[var]
    plot_title.append(
        f"{data_ie[var].attrs['long_name']} [{data_ie[var].attrs['units']}]"
    )

data_ie_df.set_index("time", inplace=True)

data_ie_df.plot(
    subplots=True,
    layout=(4, 1),
    figsize=(12, 11),
    legend=False,
    xlabel="",
    title=plot_title,
    linewidth=0.5,
)

plt.tight_layout()
plt.show()

data_ie = data_ie.sel(time=slice("1997", "1999"))

data_ie_df = pd.DataFrame({"time": data_ie["time"]})
# configure plot title
plot_title = []
for var in data_ie.data_vars:
    data_ie_df[var] = data_ie[var]
    plot_title.append(
        f"{data_ie[var].attrs['long_name']} [{data_ie[var].attrs['units']}]"
    )

data_ie_df.set_index("time", inplace=True)

data_ie_df.plot(
    subplots=True,
    layout=(4, 1),
    figsize=(12, 11),
    legend=False,
    xlabel="",
    title=plot_title,
)

plt.tight_layout()
plt.show()

# ### Box plots

data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest").sel(
    time=slice("1976", "2005")
)

data_ie_df = pd.DataFrame({"time": data_ie["time"]})
for var in data_ie.data_vars:
    data_ie_df[var] = data_ie[var]
data_ie_df.set_index("time", inplace=True)

fig, axs = plt.subplots(2, 2, figsize=(12, 4))
for ax, var in zip(axs.flat, data_ie.data_vars):
    data_ie_df.plot.box(
        column=var,
        vert=False,
        showmeans=True,
        ax=ax,
        patch_artist=True,
        color={
            "medians": "Crimson",
            "whiskers": "DarkSlateGrey",
            "caps": "DarkSlateGrey",
        },
        boxprops={"facecolor": "Lavender", "color": "DarkSlateGrey"},
        meanprops={
            "markeredgecolor": "DarkSlateGrey",
            "marker": "d",
            "markerfacecolor": (1, 1, 0, 0),  # transparent
        },
        flierprops={
            "alpha": 0.5,
            "markeredgecolor": "LightSteelBlue",
            "zorder": 1,
        },
    )
    ax.set_title(
        f"{data_ie[var].attrs['long_name']} [{data_ie[var].attrs['units']}]"
    )
    ax.set(yticklabels=[])
plt.tight_layout()
plt.show()

data_ie_df = data_ie_df[["PP"]].resample("A").sum()
data_ie_df.set_index(data_ie_df.index.year, inplace=True)

data_ie_df.plot.bar(figsize=(12, 4), legend=False, xlabel="")
plt.title("Total precipitation [mm year⁻¹]")
plt.tight_layout()
plt.show()

data_ie_df.diff().plot.hist(
    bins=15, edgecolor="darkslategrey", legend=False, alpha=0.75, hatch="///"
)
plt.show()

data_ie_df.plot.hist(
    bins=15, edgecolor="darkslategrey", legend=False, alpha=0.75, hatch="///"
)
plt.show()
