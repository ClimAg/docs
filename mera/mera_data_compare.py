#!/usr/bin/env python
# coding: utf-8

# # Met Éireann Reanalysis - compare variables
#
# <https://www.met.ie/climate/available-data/mera>
#
# Conversion table for accumulated variables:
# <https://confluence.ecmwf.int/pages/viewpage.action?pageId=197702790>

# import libraries
import glob
import os
from datetime import datetime, timezone
from itertools import chain

import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pooch
import xarray as xr

import climag.plot_configs as cplt

# Moorepark, Fermoy met station coords
LON, LAT = -8.26389, 52.16389

# transform coordinates from lon/lat to Lambert Conformal Conic
XLON, YLAT = cplt.lambert_conformal.transform_point(
    x=LON, y=LAT, src_crs=ccrs.PlateCarree()
)

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")

# directory of processed MÉRA netCDF files
DATA_DIR = os.path.join("/run/media/nms/MyPassport", "MERA", "netcdf")

URL = "https://cli.fusio.net/cli/climate_data/webdata/dly575.csv"
FILE_NAME = "moorepark.csv"
DATA_FILE = os.path.join("data", "met", "MetEireann", FILE_NAME)
os.makedirs(os.path.join("data", "met", "MetEireann"), exist_ok=True)

# download Moorepark met data if necessary
if not os.path.isfile(DATA_FILE):
    pooch.retrieve(
        url=URL,
        known_hash=None,
        fname=FILE_NAME,
        path=os.path.join("data", "met", "MetEireann"),
    )

    with open(f"{DATA_FILE[:-4]}.txt", "w", encoding="utf-8") as outfile:
        outfile.write(
            f"Data downloaded on: {datetime.now(tz=timezone.utc)}\n"
            f"Download URL: {URL}"
        )

# view file
os.system(f"sed -n -e 1,26p {DATA_FILE}")

df = pd.read_csv(DATA_FILE, skiprows=24, parse_dates=["date"])
df.set_index("date", inplace=True)
df = df.loc["2003":"2005"]
# handle missing data
df.replace(" ", np.nan, inplace=True)

df.head()

# ## Global irradiance

var = "117_105_0_4"
file_list = list(
    chain(
        *list(
            glob.glob(os.path.join(DATA_DIR, f"{var}_FC3hr", e))
            for e in [f"*{i}*{var}_FC3hr*" for i in range(2003, 2006)]
        )
    )
)
data = xr.open_mfdataset(file_list, chunks="auto", decode_coords="all")

# note that the units are incorrect; it should be J m-2
data

# convert to W m-2
var = "grad"
data_attrs = data[var].attrs  # copy var attributes
data_crs = data.rio.crs  # copy CRS
data[var] = data[var] / (3 * 3600)

# resample to daily - take the mean
time_attrs = data["time"].attrs
data_d = data.resample(time="D").mean()
data_d[var].attrs = data_attrs  # reassign attributes
data_d["time"].attrs = time_attrs
data_d[var].attrs["units"] = "W m⁻²"  # update attributes
data_d.rio.write_crs(data_crs, inplace=True)  # reassign CRS

# extract data for the nearest grid cell to the point
data_tsd = data_d.sel({"x": XLON, "y": YLAT}, method="nearest")

data_tsd

# convert to dataframe for plotting
data_df = pd.DataFrame({"time": data_tsd["time"]})
data_df[f"{var}"] = data_tsd[var]
data_df.set_index("time", inplace=True)
# met data - convert to W m-2
df_plot = df[["glorad"]].copy()
df_plot["glorad"] = (
    df_plot["glorad"].astype(float) / (1 / 100**2) / (24 * 3600)
)

# plot
ax = data_df.plot(
    figsize=(12, 4.5),
    y=var,
    color="lightslategrey",
    alpha=0.7,
    linewidth=2,
    label="MÉRA",
)
df_plot.plot(
    ax=ax, y="glorad", color="crimson", linewidth=0.75, label="Station"
)
plt.tight_layout()
plt.ylabel(
    data_d[var].attrs["long_name"] + " [" + data_d[var].attrs["units"] + "]"
)
plt.xlabel("")
plt.show()

# map
plt.figure(figsize=(9, 7))
ax = plt.axes(projection=cplt.lambert_conformal)
data_d.isel(time=90, height=0)[var].plot.contourf(
    ax=ax,
    robust=True,
    cmap="Spectral_r",
    x="x",
    y="y",
    levels=10,
    transform=cplt.lambert_conformal,
    cbar_kwargs={
        "label": (
            data_d[var].attrs["long_name"]
            + " ["
            + data_d[var].attrs["units"]
            + "]"
        )
    },
)
ax.gridlines(
    draw_labels=dict(bottom="x", left="y"),
    color="lightslategrey",
    linewidth=0.5,
    x_inline=False,
    y_inline=False,
)
ax.coastlines(resolution="10m", color="darkslategrey", linewidth=0.75)
ax.set_title(str(data_d.isel(time=90, height=0)["time"].values))
plt.tight_layout()
plt.show()

# ## Total precipitation

var = "61_105_0_4"
file_list = list(
    chain(
        *list(
            glob.glob(os.path.join(DATA_DIR, f"{var}_FC3hr", e))
            for e in [f"*{i}*{var}_FC3hr*" for i in range(2003, 2006)]
        )
    )
)
data = xr.open_mfdataset(file_list, chunks="auto", decode_coords="all")

data

# resample to daily - take the sum
var = "tp"
data_attrs = data[var].attrs
time_attrs = data["time"].attrs
data_crs = data.rio.crs
data_d = data.resample(time="D").sum()
data_d[var].attrs = data_attrs
data_d["time"].attrs = time_attrs
data_d[var].attrs["units"] = "mm day⁻¹"
data_d.rio.write_crs(data_crs, inplace=True)

# clip to Ireland's boundary to remove NaNs after summing
data_d = data_d.rio.clip(
    ie.buffer(1).to_crs(cplt.lambert_conformal), all_touched=True
)

data_d

# extract data for the nearest grid cell to the point
data_tsd = data_d.sel({"x": XLON, "y": YLAT}, method="nearest")

data_tsd

# convert to dataframe for plotting
data_df = pd.DataFrame({"time": data_tsd["time"]})
data_df[f"{var}"] = data_tsd[var]
data_df.set_index("time", inplace=True)
# met data
df_plot = df[["rain"]].copy()
df_plot["rain"] = df_plot["rain"].astype(float)

# plot
ax = data_df.plot(
    figsize=(12, 4.5),
    y=var,
    color="lightslategrey",
    alpha=0.7,
    linewidth=2,
    label="MÉRA",
)
df_plot.plot(ax=ax, y="rain", color="crimson", linewidth=0.75, label="Station")
plt.tight_layout()
plt.ylabel(
    data_d[var].attrs["long_name"] + " [" + data_d[var].attrs["units"] + "]"
)
plt.xlabel("")
plt.show()

# map
plt.figure(figsize=(9, 7))
ax = plt.axes(projection=cplt.lambert_conformal)
data_d.isel(time=90, height=0)[var].plot.contourf(
    ax=ax,
    robust=True,
    cmap=cplt.cmap_mako_r,
    x="x",
    y="y",
    levels=10,
    transform=cplt.lambert_conformal,
    cbar_kwargs={
        "label": (
            data_d[var].attrs["long_name"]
            + " ["
            + data_d[var].attrs["units"]
            + "]"
        )
    },
)
ax.gridlines(
    draw_labels=dict(bottom="x", left="y"),
    color="lightslategrey",
    linewidth=0.5,
    x_inline=False,
    y_inline=False,
)
ax.coastlines(resolution="10m", color="darkslategrey", linewidth=0.75)
ax.set_title(str(data_d.isel(time=90, height=0)["time"].values))
plt.tight_layout()
plt.show()

# ## Maximum temperature

var = "15_105_2_2"
file_list = list(
    chain(
        *list(
            glob.glob(os.path.join(DATA_DIR, f"{var}_FC3hr", e))
            for e in [f"*{i}*{var}_FC3hr*" for i in range(2003, 2006)]
        )
    )
)
data = xr.open_mfdataset(file_list, decode_coords="all", chunks="auto")

data

# convert to deg C
var = "tmax"
data_attrs = data[var].attrs
data_crs = data.rio.crs
data[var] = data[var] - 273.15

# resample to daily - take the max
time_attrs = data["time"].attrs
data_d = data.resample(time="D").max()
data_d[var].attrs = data_attrs  # reassign attributes
data_d["time"].attrs = time_attrs
data_d[var].attrs["units"] = "°C"  # update attributes
data_d.rio.write_crs(data_crs, inplace=True)  # reassign CRS

# extract data for the nearest grid cell to the point
data_tsd = data_d.sel({"x": XLON, "y": YLAT}, method="nearest")

data_tsd

# convert to dataframe for plotting
data_df = pd.DataFrame({"time": data_tsd["time"]})
data_df[f"{var}"] = data_tsd[var]
data_df.set_index("time", inplace=True)
# met data
df_plot = df[["maxtp"]].copy()
df_plot["maxtp"] = df_plot["maxtp"].astype(float)

# plot
ax = data_df.plot(
    figsize=(12, 4.5),
    y=var,
    color="lightslategrey",
    alpha=0.7,
    linewidth=2,
    label="MÉRA",
)
df_plot.plot(
    ax=ax, y="maxtp", color="crimson", linewidth=0.75, label="Station"
)
plt.tight_layout()
plt.ylabel(
    data_d[var].attrs["long_name"] + " [" + data_d[var].attrs["units"] + "]"
)
plt.xlabel("")
plt.show()

# map
plt.figure(figsize=(9, 7))
ax = plt.axes(projection=cplt.lambert_conformal)
data_d.isel(time=90, height=0)[var].plot.contourf(
    ax=ax,
    robust=True,
    cmap="Spectral_r",
    x="x",
    y="y",
    levels=10,
    transform=cplt.lambert_conformal,
    cbar_kwargs={
        "label": (
            data_d[var].attrs["long_name"]
            + " ["
            + data_d[var].attrs["units"]
            + "]"
        )
    },
)
ax.gridlines(
    draw_labels=dict(bottom="x", left="y"),
    color="lightslategrey",
    linewidth=0.5,
    x_inline=False,
    y_inline=False,
)
ax.coastlines(resolution="10m", color="darkslategrey", linewidth=0.75)
ax.set_title(str(data_d.isel(time=90, height=0)["time"].values))
plt.tight_layout()
plt.show()

print("Last updated:", datetime.now(tz=timezone.utc))
