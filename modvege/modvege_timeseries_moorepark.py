#!/usr/bin/env python
# coding: utf-8

# # ModVege results - Moorepark time series distribution

# import libraries
import os
import glob
import itertools
import numpy as np
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
from dask.distributed import Client
import climag.plot_configs as cplt
import climag.plot_facet_maps as cfacet

print("Last updated:", datetime.now(tz=timezone.utc))

client = Client(n_workers=2, threads_per_worker=4, memory_limit="3GB")

client

# Moorepark met station coords
LON, LAT = -8.26389, 52.16389

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries.gpkg")
ie_bbox = gpd.read_file(GPKG_BOUNDARY, layer="ne_10m_land_2157_IE_BBOX_DIFF")

BASE_DIR = os.path.join("data", "ModVege", "EURO-CORDEX")
TEMP_DIR = os.path.join(BASE_DIR, "stats")
os.makedirs(TEMP_DIR, exist_ok=True)

# exp, model = "rcp45", "EC-EARTH"

datasets = {}

for exp, model, data in itertools.product(
    ["historical", "rcp45", "rcp85"],
    ["CNRM-CM5", "EC-EARTH", "HadGEM2-ES", "MPI-ESM-LR"],
    ["EURO-CORDEX", "HiResIreland"],
):
    # auto-rechunking may cause NotImplementedError with object dtype
    # where it will not be able to estimate the size in bytes of object data
    if model == "HadGEM2-ES":
        CHUNKS = 300
    else:
        CHUNKS = "auto"

    datasets[f"{data}_{model}_{exp}"] = xr.open_mfdataset(
        glob.glob(
            os.path.join(
                "data",
                "ModVege",
                data,
                exp,
                model,
                f"*{data}*{model}*{exp}*.nc",
            )
        ),
        chunks=CHUNKS,
        decode_coords="all",
    )

    # convert HadGEM2-ES data back to 360-day calendar
    # this ensures that the correct weighting is applied when calculating
    # the weighted average
    if model == "HadGEM2-ES":
        datasets[f"{data}_{model}_{exp}"] = datasets[
            f"{data}_{model}_{exp}"
        ].convert_calendar("360_day", align_on="year")

# remove spin-up year
for key in datasets.keys():
    if "historical" in key:
        datasets[key] = datasets[key].sel(time=slice("1976", "2005"))
    else:
        datasets[key] = datasets[key].sel(time=slice("2041", "2070"))
    # # normalise to keep only date in time
    # datasets[key]["time"] = datasets[key].indexes["time"].normalize()

list(datasets.keys())

datasets["EURO-CORDEX_EC-EARTH_rcp45"]

varlist = ["bm", "pgro", "gro", "i_bm"]

# ## Box plots

data_all = cplt.boxplot_data(
    datasets=datasets, varlist=varlist, lonlat=(LON, LAT)
)

for var in varlist:
    cplt.boxplot_all(
        data=data_all[var],
        var=var,
        title=(
            datasets["EURO-CORDEX_EC-EARTH_rcp45"][var].attrs["long_name"]
            + f" [{datasets['EURO-CORDEX_EC-EARTH_rcp45'][var].attrs['units']}]"
            f" at Moorepark ({LON}, {LAT})"
        ),
    )

# ## Histograms

for var in varlist:
    data_pivot = pd.pivot_table(
        data_all[var], values=var, columns="legend", index=data_all[var].index
    )
    data_pivot.plot(
        kind="hist",
        subplots=True,
        figsize=(10, 18),
        bins=50,
        sharex=True,
        sharey=True,
        layout=(8, 3),
        title=(
            datasets["EURO-CORDEX_EC-EARTH_rcp45"][var].attrs["long_name"]
            + f" [{datasets['EURO-CORDEX_EC-EARTH_rcp45'][var].attrs['units']}]"
            f" at Moorepark ({LON}, {LAT})"
        ),
    )
    plt.tight_layout()
    plt.show()
