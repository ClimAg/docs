#!/usr/bin/env python
# coding: utf-8

# import libraries
import os

import xarray as xr

DATA_DIR_BASE = os.path.join("data", "HiResIreland")

data = xr.open_dataset(
    os.path.join("data", "HiResIreland", "lfsd1981012712.nc"),
    decode_coords="all",
)

data
