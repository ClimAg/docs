#!/usr/bin/env python
# coding: utf-8

# # ModVege results - hist/rcp comparisons for EURO-CORDEX

# import libraries
import glob
import importlib
import itertools
import os
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
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

datasets = {}

for exp, model, data in itertools.product(
    ["historical", "rcp45", "rcp85"],
    ["CNRM-CM5", "EC-EARTH", "HadGEM2-ES", "MPI-ESM-LR"],
    ["EURO-CORDEX"]
    # ["EURO-CORDEX", "HiResIreland"]
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

# ## Seasonal maps - hist/rcp diff

# subset data for a particular driving model
dataset_ecearth = {}
for key in datasets.keys():
    if "EC-EARTH" in key:
        dataset_ecearth[key.split("_")[2]] = datasets[key]

plotting_data = cfacet.weighted_average_season_exp(dataset_ecearth)

cfacet.plot_weighted_average_season_exp(
    driving_model_data=dataset_ecearth,
    plotting_data=plotting_data,
    var="gro",
    boundary_data=ie_bbox,
    levels=([0 + 15 * n for n in range(13)], [-29 + 2 * n for n in range(30)]),
    ticks=(None, [-25 + 5 * n for n in range(11)]),
)

importlib.reload(cfacet)
