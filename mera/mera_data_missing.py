#!/usr/bin/env python
# coding: utf-8

# # Met Éireann Reanalysis - dealing with missing data

# import libraries
import glob
import os
from datetime import datetime, timezone

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr

import climag.plot_configs as cplt

# directory of processed MÉRA netCDF files
DATA_DIR = os.path.join("/run/media/nms/MyPassport", "MERA", "netcdf_day")

# ## Find timestamps with missing data

ds_grib = xr.open_dataset(
    "/run/media/nms/MyPassport/MERA/grib/117_105_0_4_FC3hr/"
    "MERA_PRODYEAR_2013_05_117_105_0_4_FC3hr",
    chunks="auto",
    decode_coords="all",
    engine="cfgrib",
)

ds_grib

ds_nc = xr.open_dataset(
    "/run/media/nms/MyPassport/MERA/netcdf/117_105_0_4_FC3hr/"
    "MERA_PRODYEAR_2013_05_117_105_0_4_FC3hr.nc",
    chunks="auto",
    decode_coords="all",
)

ds_nc

# ## Read radiation daily data

ds = xr.open_dataset(
    os.path.join(DATA_DIR, "MERA_117_105_0_4_day.nc"),
    chunks="auto",
    decode_coords="all",
)
ds = ds.isel(height=0)

ds2 = xr.open_dataset(
    os.path.join(DATA_DIR, "MERA_111_105_0_4_day.nc"),
    chunks="auto",
    decode_coords="all",
)
ds2 = ds2.isel(height=0)

ds

ds2

# ## Visualise

# Moorepark, Fermoy met station coords
LON, LAT = -8.26389, 52.16389

# transform coordinates from lon/lat to Lambert Conformal Conic
XLON, YLAT = cplt.lambert_conformal.transform_point(
    x=LON, y=LAT, src_crs=ccrs.PlateCarree()
)


def plot_map(data, var, cmap="Spectral_r"):
    """
    Helper function for plotting maps
    """

    plt.figure(figsize=(9, 7))
    ax = plt.axes(projection=cplt.lambert_conformal)
    data.isel(time=120)[var].plot.contourf(
        ax=ax,
        robust=True,
        x="x",
        y="y",
        levels=10,
        transform=cplt.lambert_conformal,
        cmap=cmap,
        cbar_kwargs={
            "label": (
                data[var].attrs["long_name"]
                + " ["
                + data[var].attrs["units"]
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
    ax.set_title(str(data.isel(time=90)["time"].values))
    plt.tight_layout()
    plt.show()


def plot_ts(data, var, sub=True):
    """
    Helper function for plotting time series
    """

    plt.figure(figsize=(12, 4))
    data_ts = data.sel({"x": XLON, "y": YLAT}, method="nearest")
    if sub:
        data_ts = data_ts.sel(time=slice("2013-04", "2013-06"))
    plt.plot(data_ts["time"], data_ts[var])
    # plt.title(
    #     data[var].attrs["long_name"] + " [" + data[var].attrs["units"] + "]"
    # )
    plt.tight_layout()
    plt.show()


ds_ = ds.sel({"x": XLON, "y": YLAT}, method="nearest")
ds2_ = ds2.sel({"x": XLON, "y": YLAT}, method="nearest")
ds_ = ds_.sel(time=slice("2013-04", "2013-06"))
ds2_ = ds2_.sel(time=slice("2013-04", "2013-06"))
fig = plt.figure(figsize=(12, 4))
plt.plot(ds_["time"], ds_["grad"], color="lightgrey")
plt.plot(ds2_["time"], ds2_["nswrs"], color="crimson", linewidth=0.5)

# plt.title(
#     data[var].attrs["long_name"] + " [" + data[var].attrs["units"] + "]"
# )
plt.tight_layout()
plt.show()

# ## Ratio

ds3 = ds.copy()
ds3 = ds3.assign(nswrs=ds2["nswrs"])
ds3 = ds3.assign(ratio=ds3["grad"] / ds3["nswrs"])

ds3

ds3_ = ds3.sel({"x": XLON, "y": YLAT}, method="nearest")
# ds3_ = ds3_.sel(time=slice("2013-04", "2013-06"))
fig = plt.figure(figsize=(12, 4))
plt.plot(ds3_["time"], ds3_["ratio"])
plt.tight_layout()
plt.show()

ds3.mean(dim="time")["ratio"].plot()
plt.tight_layout()
plt.show()

ds3["ratio"].mean(dim=None).values

(ds3["grad"] / ds3["nswrs"]).mean(dim=None).values

# ## Adjust

ds2.assign(grad=ds2["nswrs"] * 1.2155399)

ds3 = ds3.fillna(ds2.assign(grad=ds2["nswrs"] * 1.2155399))

ds_ = ds.sel({"x": XLON, "y": YLAT}, method="nearest")
ds_ = ds_.sel(time=slice("2013-04", "2013-06"))
ds2_ = ds2.sel({"x": XLON, "y": YLAT}, method="nearest")
ds2_ = ds2_.sel(time=slice("2013-04", "2013-06"))
ds3_ = ds3.sel({"x": XLON, "y": YLAT}, method="nearest")
ds3_ = ds3_.sel(time=slice("2013-04", "2013-06"))
fig = plt.figure(figsize=(12, 4))
plt.plot(ds3_["time"], ds3_["grad"])
plt.plot(ds_["time"], ds_["grad"], color="lightgrey", linewidth=2.5)
plt.plot(ds2_["time"], ds2_["nswrs"], color="crimson", linewidth=0.5)

# plt.title(
#     data[var].attrs["long_name"] + " [" + data[var].attrs["units"] + "]"
# )
plt.tight_layout()
plt.show()
