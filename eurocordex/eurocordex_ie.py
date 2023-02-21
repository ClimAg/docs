#!/usr/bin/env python
# coding: utf-8

# # Subset EURO-CORDEX data for Ireland

# import libraries
import os
from datetime import datetime, timezone
import geopandas as gpd
import intake
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
from dask.distributed import Client
import climag.plot_configs as cplt

print("Last updated:", datetime.now(tz=timezone.utc))

client = Client(n_workers=3, threads_per_worker=4, memory_limit="2GB")

client

DATA_DIR_BASE = os.path.join("data", "EURO-CORDEX")

# directory to store outputs
DATA_DIR = os.path.join(DATA_DIR_BASE, "IE")
os.makedirs(DATA_DIR, exist_ok=True)

# Valentia Observatory met station coords
LON, LAT = -10.24333, 51.93806

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")
ie_bbox = gpd.read_file(
    GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE_BBOX_DIFF"
)

# ## Reading the local catalogue

JSON_FILE_PATH = os.path.join(
    DATA_DIR_BASE, "eurocordex_eur11_local_disk.json"
)

cordex_eur11_cat = intake.open_esm_datastore(JSON_FILE_PATH)

list(cordex_eur11_cat)

cordex_eur11_cat

cordex_eur11_cat.df.shape

cordex_eur11_cat.df.head()

# ## Read a subset (rcp45)

cordex_eur11 = cordex_eur11_cat.search(
    experiment_id="rcp45", driving_model_id="ICHEC-EC-EARTH"
)

cordex_eur11

cordex_eur11.df

data = xr.open_mfdataset(
    list(cordex_eur11.df["uri"]), chunks="auto", decode_coords="all"
)

# using Valentia Observatory met station coordinates
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

data

# copy time_bnds coordinates
data_time_bnds = data.coords["time_bnds"]

# copy CRS
data_crs = data.rio.crs

data_crs

# subset for reference period and spin-up year
data = data.sel(time=slice("2040", "2070"))

data

# ### Ireland subset

# clip to Ireland's boundary
data = data.rio.clip(ie.buffer(500).to_crs(data_crs))

# reassign time_bnds
data.coords["time_bnds"] = data_time_bnds

data

# ### Calculate photosynthetically active radiation

# Papaioannou et al. (1993) - irradiance ratio
data = data.assign(PAR=data["rsds"] * 0.473)

data

# ### Calculate net downward shortwave radiation

# assume an albedo of 0.23 (Allen et al., 1998)
data = data.assign(RSN=data["rsds"] * (1 - 0.23))

data

# ### Convert units

for v in data.data_vars:
    var_attrs = data[v].attrs  # extract attributes
    if v == "tas":
        var_attrs["units"] = "°C"
        data[v] = data[v] - 273.15
        var_attrs["note"] = "Converted from K to °C by subtracting 273.15"
    elif v in ("PAR", "RSN", "rsds"):
        var_attrs["units"] = "MJ m⁻² day⁻¹"
        data[v] = data[v] * (60 * 60 * 24 / 1e6)
        if v == "PAR":
            var_attrs[
                "long_name"
            ] = "Surface Photosynthetically Active Radiation"
            var_attrs["note"] = (
                "Calculated by multiplying 'rsds' with an irradiance "
                "ratio of 0.473 based on Papaioannou et al. (1993); "
                "converted from W m⁻² to MJ m⁻² day⁻¹ by multiplying "
                "0.0864 based on the FAO Irrigation and Drainage Paper "
                "No. 56 (Allen et al., 1998, p. 45)"
            )
        elif v == "RSN":
            var_attrs["long_name"] = "Surface Net Downward Shortwave Radiation"
    elif v in ("pr", "evspsblpot"):
        var_attrs["units"] = "mm day⁻¹"
        data[v] = data[v] * 60 * 60 * 24
        var_attrs["note"] = (
            "Converted from kg m⁻² s⁻¹ to mm day⁻¹ by multiplying 86,400,"
            " assuming a water density of 1,000 kg m⁻³"
        )
    data[v].attrs = var_attrs  # reassign attributes

# rename variables
data = data.rename({"tas": "T", "rsds": "RS", "pr": "PP", "evspsblpot": "PET"})

# assign dataset name
for x in ["CNRM-CM5", "EC-EARTH", "HadGEM2-ES", "MPI-ESM-LR"]:
    if x in data.attrs["driving_model_id"]:
        data.attrs[
            "dataset"
        ] = f"IE_EURO-CORDEX_RCA4_{x}_{data.attrs['experiment_id']}"

# assign attributes to the data
data.attrs["comment"] = (
    "This dataset has been clipped with the Island of Ireland's boundary and "
    "units have been converted. "
    "Last updated: "
    + str(datetime.now(tz=timezone.utc))
    + " by nstreethran@ucc.ie."
)

data

# reassign CRS
data.rio.write_crs(data_crs, inplace=True)

data.rio.crs

# ### Monthly averages

cplt.plot_averages(
    data=data.sel(time=slice("2041", "2070")),
    var="T",
    averages="month",
    boundary_data=ie_bbox,
    cbar_levels=[3 + 1 * n for n in range(13)],
)

for var in data.data_vars:
    cplt.plot_averages(
        data=data.sel(time=slice("2041", "2070")),
        var=var,
        averages="month",
        boundary_data=ie_bbox,
        cbar_levels=12,
    )

# ### Seasonal averages

for var in data.data_vars:
    cplt.plot_averages(
        data=data.sel(time=slice("2041", "2070")),
        var=var,
        averages="season",
        boundary_data=ie_bbox,
        cbar_levels=12,
    )

# ### Point subset

data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest").sel(
    time=slice("2041", "2070")
)

data_ie

for var in data.data_vars:
    plt.figure(figsize=(12, 4))
    plt.plot(data_ie["time"], data_ie[var], linewidth=0.5)
    plt.title(f"{data_ie.attrs['dataset']}, lon={LON}, lat={LAT}")
    plt.ylabel(
        f"{data_ie[var].attrs['long_name']}\n[{data_ie[var].attrs['units']}]"
    )
    plt.tight_layout()
    plt.show()

data_ie = data_ie.sel(time=slice("2054", "2056"))

for var in data.data_vars:
    plt.figure(figsize=(12, 4))
    plt.plot(data_ie["time"], data_ie[var], linewidth=1)
    plt.title(f"{data_ie.attrs['dataset']}, lon={LON}, lat={LAT}")
    plt.ylabel(
        f"{data_ie[var].attrs['long_name']}\n[{data_ie[var].attrs['units']}]"
    )
    plt.tight_layout()
    plt.show()

data_ie_df = pd.DataFrame({"time": data_ie["time"]})
for var in ["RS", "RSN", "PAR"]:
    data_ie_df[var] = data_ie[var]

data_ie_df.set_index("time", inplace=True)

data_ie_df.plot(figsize=(12, 4), colormap="viridis", xlabel="")

plt.tight_layout()
plt.show()

data_ie_df = pd.DataFrame({"time": data_ie["time"]})
# configure plot title
plot_title = []
for var in ["T", "PP", "PET", "PAR"]:
    data_ie_df[var] = data_ie[var]
    plot_title.append(
        f"{data_ie[var].attrs['long_name']} [{data_ie[var].attrs['units']}]"
    )

data_ie_df.set_index("time", inplace=True)

data_ie_df.plot(
    subplots=True,
    layout=(4, 1),
    figsize=(9, 11),
    legend=False,
    xlabel="",
    title=plot_title,
)

plt.tight_layout()
plt.show()
