#!/usr/bin/env python
# coding: utf-8

# import libraries
import os
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
from dask.distributed import Client
import climag.plot_configs as cplt

client = Client(n_workers=3, threads_per_worker=4, memory_limit="2GB")

client

DATA_DIR_BASE = os.path.join("data", "EURO-CORDEX", "IE")

# Valentia Observatory met station coords
LON, LAT = -10.24333, 51.93806

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")
ie_bbox = gpd.read_file(
    GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE_BBOX_DIFF"
)

# ## HadGEM2-ES - no chunking

data = xr.open_dataset(
    os.path.join(
        DATA_DIR_BASE, "IE_EURO-CORDEX_RCA4_HadGEM2-ES_historical.nc"
    ),
    decode_coords="all",
)

data

data.rio.crs

cplt.plot_averages(
    data=data.sel(time=slice("1976", "2005")),
    var="T",
    averages="month",
    boundary_data=ie_bbox,
    cbar_levels=[3 + 1 * n for n in range(13)],
)

# ## MPI-ESM-LR - with chunking

data = xr.open_dataset(
    os.path.join(
        DATA_DIR_BASE, "IE_EURO-CORDEX_RCA4_MPI-ESM-LR_historical.nc"
    ),
    decode_coords="all",
    chunks="auto",
)

data

data.rio.crs

cplt.plot_averages(
    data=data.sel(time=slice("1976", "2005")),
    var="T",
    averages="month",
    boundary_data=ie_bbox,
    cbar_levels=[3 + 1 * n for n in range(13)],
)
