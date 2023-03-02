#!/usr/bin/env python
# coding: utf-8

# # Box plots

import os
import glob
from datetime import datetime, timezone
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import xarray as xr
import climag.plot_configs as cplt

DATA_DIR = os.path.join("data", "ModVege")

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")

# Moorepark met station coords
LON, LAT = -8.26389, 52.16389

outputs = {}

for exp in ["historical", "rcp45", "rcp85"]:
    # HiResIreland
    outputs[f"hiresireland_{exp}"] = xr.open_mfdataset(
        glob.glob(
            os.path.join(DATA_DIR, "HiResIreland", exp, "EC-EARTH", "*.nc")
        ),
        chunks="auto",
        decode_coords="all",
    )

    # EURO-CORDEX
    outputs[f"eurocordex_{exp}"] = xr.open_mfdataset(
        glob.glob(
            os.path.join(DATA_DIR, "EURO-CORDEX", exp, "EC-EARTH", "*.nc")
        ),
        chunks="auto",
        decode_coords="all",
    )

outputs["eurocordex_historical"]

inputs = {}

for exp in ["historical", "rcp45", "rcp85"]:
    # HiResIreland
    inputs[f"hiresireland_{exp}"] = xr.open_dataset(
        glob.glob(
            os.path.join("data", "HiResIreland", "IE", f"*EC-EARTH*{exp}*.nc")
        )[0],
        chunks="auto",
        decode_coords="all",
    )

    # EURO-CORDEX
    inputs[f"eurocordex_{exp}"] = xr.open_dataset(
        glob.glob(
            os.path.join("data", "EURO-CORDEX", "IE", f"*EC-EARTH*{exp}*.nc")
        )[0],
        chunks="auto",
        decode_coords="all",
    )

inputs["eurocordex_historical"]

# ## Box plots

cplt.plot_box(data=inputs, lonlat=(LON, LAT), var="PP")

cplt.plot_box(data=inputs, lonlat=(LON, LAT), var="PP", fliers=True)

cplt.plot_box_multi(
    data=inputs, lonlat=(LON, LAT), varlist=["T", "PAR", "PET", "PP"]
)

cplt.plot_box_multi(
    data=inputs,
    lonlat=(LON, LAT),
    varlist=["T", "PAR", "PET", "PP"],
    fliers=True,
)

cplt.plot_box_multi(
    data=outputs, lonlat=(LON, LAT), varlist=["gro", "pgro", "bm", "i_bm"]
)

cplt.plot_box_multi(
    data=outputs,
    lonlat=(LON, LAT),
    varlist=["gro", "pgro", "bm", "i_bm"],
    fliers=True,
)
