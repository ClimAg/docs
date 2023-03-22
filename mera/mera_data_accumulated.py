#!/usr/bin/env python
# coding: utf-8

# # Met Éireann Reanalysis
#
# <https://www.met.ie/climate/available-data/mera>

# import libraries
import os
from datetime import date, datetime, timezone
import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.units as munits
import numpy as np
import pooch
import xarray as xr
import glob
import climag.plot_configs as cplt
import pandas as pd
from itertools import chain

LON, LAT = -10.24333, 51.93806  # Valentia Observatory

# transform coordinates from lon/lat to Lambert Conformal Conic
XLON, YLAT = cplt.lambert_conformal.transform_point(
    x=LON, y=LAT, src_crs=ccrs.PlateCarree()
)

# Ireland boundary (derived from NUTS 2021)
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")

# directory of MERA GRIB files
DATA_DIR = os.path.join("/run/media/nms/Elements", "MERA", "grib")
NC_DIR = os.path.join("/run/media/nms/MyPassport", "MERA", "netcdf")

# ## Global radiation

for var in ["117_105_0_4"]:
    # directory to store temporary files
    TEMP_DIR = os.path.join(DATA_DIR, f"{var}_FC3hr", "temp")
    os.makedirs(TEMP_DIR, exist_ok=True)
    # directory to store netCDFs
    os.makedirs(os.path.join(NC_DIR, f"{var}_FC3hr"), exist_ok=True)

    # list of files; 1981 to 2005
    file_list = list(
        chain(
            *list(
                glob.glob(os.path.join(DATA_DIR, f"{var}_FC3hr", e))
                for e in [f"*{i}*{var}_FC3hr*" for i in range(2010, 2011)]
            )
        )
    )

    for f in file_list:
        # if the GRIB file is archived, decompress it
        if f.endswith(".bz2"):
            # GRIB file path
            file_name = os.path.split(f)[1][:-4]
            gf = os.path.join(TEMP_DIR, file_name)
            # extract file
            with bz2.BZ2File(f, "rb") as in_file:
                with open(gf, "wb") as out_file:
                    shutil.copyfileobj(in_file, out_file)
        else:
            # if not compressed, copy GRIB file to temp dir
            os.system(f"cp {f} {TEMP_DIR}")
            file_name = os.path.split(f)[1]
            gf = os.path.join(TEMP_DIR, file_name)

        # open the GRIB file to get data length and variable attributes
        data = xr.open_dataset(
            gf, decode_coords="all", chunks="auto", engine="cfgrib"
        )
        data_varname = list(data.data_vars)[0]
        data_attrs = data[data_varname].attrs

        # keep only the third forecast step and convert to netCDF
        os.system(
            "cdo -s -f nc4c -copy "
            # f"-seltimestep,3/{len(data['time']) * 3}/3 "
            f"{gf} {gf}.nc"
        )

        # assign variable attributes and clip to Ireland's boundary
        data = xr.open_dataset(f"{gf}.nc", decode_coords="all", chunks="auto")
        data = data.rename({list(data.data_vars)[0]: data_varname})
        data[data_varname].attrs = data_attrs
        data = data.rio.clip(
            ie.buffer(1).to_crs(cplt.lambert_conformal), all_touched=True
        )
        data.to_netcdf(os.path.join(NC_DIR, f"{var}_FC3hr", file_name + ".nc"))

        # delete intermediate files
        os.system(f"rm -r {os.path.join(TEMP_DIR, '*')}")

for var in ["117_105_0_4"]:
    # directory to store temporary files
    TEMP_DIR = os.path.join(DATA_DIR, f"{var}_FC3hr", "temp")
    os.makedirs(TEMP_DIR, exist_ok=True)
    # directory to store netCDFs
    os.makedirs(os.path.join(NC_DIR, f"{var}_FC3hr"), exist_ok=True)

    # list of files; 1981 to 2005
    file_list = list(
        chain(
            *list(
                glob.glob(os.path.join(DATA_DIR, f"{var}_FC3hr", e))
                for e in [f"*{i}*{var}_FC3hr*" for i in range(2011, 2012)]
            )
        )
    )

    for f in file_list:
        # if the GRIB file is archived, decompress it
        if f.endswith(".bz2"):
            # GRIB file path
            file_name = os.path.split(f)[1][:-4]
            gf = os.path.join(TEMP_DIR, file_name)
            # extract file
            with bz2.BZ2File(f, "rb") as in_file:
                with open(gf, "wb") as out_file:
                    shutil.copyfileobj(in_file, out_file)
        else:
            # if not compressed, copy GRIB file to temp dir
            os.system(f"cp {f} {TEMP_DIR}")
            file_name = os.path.split(f)[1]
            gf = os.path.join(TEMP_DIR, file_name)

        # open the GRIB file to get data length and variable attributes
        data = xr.open_dataset(
            gf, decode_coords="all", chunks="auto", engine="cfgrib"
        )
        data_varname = list(data.data_vars)[0]
        data_attrs = data[data_varname].attrs

        # keep only the third forecast step and convert to netCDF
        os.system(
            "cdo -s -f nc4c -copy "
            f"-seltimestep,3/{len(data['time']) * 3}/3 "
            f"{gf} {gf}.nc"
        )

        # assign variable attributes and clip to Ireland's boundary
        data = xr.open_dataset(f"{gf}.nc", decode_coords="all", chunks="auto")
        data = data.rename({list(data.data_vars)[0]: data_varname})
        data[data_varname].attrs = data_attrs
        data = data.rio.clip(
            ie.buffer(1).to_crs(cplt.lambert_conformal), all_touched=True
        )
        data.to_netcdf(os.path.join(NC_DIR, f"{var}_FC3hr", file_name + ".nc"))

        # delete intermediate files
        os.system(f"rm -r {os.path.join(TEMP_DIR, '*')}")

data_1 = xr.open_mfdataset(
    glob.glob(os.path.join(NC_DIR, "117_105_0_4_FC3hr", "*2010*FC3hr.nc")),
    decode_coords="all",
    chunks="auto",
)

data_2 = xr.open_mfdataset(
    glob.glob(os.path.join(NC_DIR, "117_105_0_4_FC3hr", "*2011*FC3hr.nc")),
    decode_coords="all",
    chunks="auto",
)

data_1

data_2

# resample to daily
var = "grad"
time_attrs = data_1["time"].attrs
data_attrs = data_1[var].attrs
data_d1 = data_1.resample(time="3H").sum()
data_d1 = data_d1.resample(time="D").mean()
# data_d1 = data_1.resample(time="D").mean()
data_d1[var].attrs = data_attrs
data_d1["time"].attrs = time_attrs

# resample to daily and convert units to deg C
var = "grad"
time_attrs = data_2["time"].attrs
data_attrs = data_2[var].attrs
data_d2 = data_2.resample(time="D").mean()
data_d2[var].attrs = data_attrs
data_d2["time"].attrs = time_attrs

# extract data for the nearest grid cell to the point
data_tsd1 = data_d1.sel(dict(x=XLON, y=YLAT), method="nearest")
data_tsd2 = data_d2.sel(dict(x=XLON, y=YLAT), method="nearest")

data_df1 = pd.DataFrame({"time": data_tsd1["time"]})
data_df1[f"{var}_1"] = data_tsd1[var]
data_df2 = pd.DataFrame({"time": data_tsd2["time"]})
data_df2[f"{var}_2"] = data_tsd2[var]

data_df = pd.concat([data_df1, data_df2])

data_df.set_index("time", inplace=True)

data_df.head()

data_df.tail()

data_df.plot(figsize=(12, 4))
plt.tight_layout()
plt.show()

# compare w/ met data
val = pd.read_csv(
    "data/met/MetEireann/dly2275.csv", skiprows=24, parse_dates=["date"]
)

# filter data
val = val[(val["date"].dt.year >= 2010) & (val["date"].dt.year <= 2011)]

val["time"] = val["date"]
val.set_index("time", inplace=True)

# convert all to W m-2
data_df["glorad"] = (
    val["glorad"].astype(float) / (1 / 100**2) / (24 * 3600)
)  # from J cm-2
data_df["grad_1"] = data_df["grad_1"].astype(float) / (3 * 3600)  # 1h
data_df["grad_2"] = data_df["grad_2"].astype(float) / (3 * 3600)  # 3h

data_df.head()

data_df.plot(figsize=(12, 4))
plt.tight_layout()
plt.show()

ax = data_df[["glorad"]].plot(
    figsize=(12, 4), linewidth=2, color="lightslategrey", alpha=0.7
)
data_df[["grad_2"]].plot(
    figsize=(12, 4), ax=ax, color="crimson", linewidth=0.5
)
plt.tight_layout()
plt.show()

# convert all to MJ m-2 day-1
data_df["glorad"] = data_df["glorad"].astype(float) * 86400 / 1e6
data_df["grad_1"] = data_df["grad_1"].astype(float) * 86400 / 1e6
data_df["grad_2"] = data_df["grad_2"].astype(float) * 86400 / 1e6

ax = data_df[["glorad"]].plot(
    figsize=(12, 4), linewidth=2, color="lightslategrey", alpha=0.7
)
data_df[["grad_2"]].plot(
    figsize=(12, 4), ax=ax, color="crimson", linewidth=0.5
)
plt.tight_layout()
plt.show()

# convert all to PAR
data_df["glorad"] = data_df["glorad"].astype(float) * 0.473
data_df["grad_1"] = data_df["grad_1"].astype(float) * 0.473
data_df["grad_2"] = data_df["grad_2"].astype(float) * 0.473

ax = data_df[["glorad"]].plot(
    figsize=(12, 4), linewidth=2, color="lightslategrey", alpha=0.7
)
data_df[["grad_2"]].plot(
    figsize=(12, 4), ax=ax, color="crimson", linewidth=0.5
)
plt.tight_layout()
plt.show()
