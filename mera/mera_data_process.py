#!/usr/bin/env python
# coding: utf-8

# # Met Éireann Reanalysis - create input data for ModVege

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

# list of netCDF variable files
var_list = [
    "11_105_2_0",  # 2 m temperature
    "61_105_0_4",  # total precipitation
    "117_105_0_4",  # global irradiance
    "PET",  # evapotranspiration
]

# dictionary to store Xarray datasets
ds = {}

for var in var_list:
    ds[var] = xr.open_mfdataset(
        glob.glob(os.path.join(DATA_DIR, f"MERA_{var}_day.nc")),
        chunks="auto",
        decode_coords="all",
    )

# obtain CRS info
data_crs = ds["11_105_2_0"].rio.crs

data_crs

# drop the height dimension from the datasets
for v in var_list[:-1]:
    ds[v] = ds[v].isel(height=0)

# ## View datasets

ds["11_105_2_0"]

ds["61_105_0_4"]

ds["117_105_0_4"]

ds["PET"]

# ## Calculate photosynthetically active radiation (PAR)

# Papaioannou et al. (1993) - irradiance ratio
ds["117_105_0_4"] = ds["117_105_0_4"].assign(
    PAR=ds["117_105_0_4"]["grad"] * 0.473
)
ds["117_105_0_4"]["PAR"].attrs[
    "long_name"
] = "Surface Photosynthetically Active Radiation"
ds["117_105_0_4"]["PAR"].attrs["units"] = "MJ m⁻² day⁻¹"

# ## Merge datasets

# merge datasets
ds = xr.combine_by_coords(
    [ds["11_105_2_0"], ds["61_105_0_4"], ds["117_105_0_4"], ds["PET"]],
    combine_attrs="drop_conflicts",
    compat="override",
)

# drop global radiation
ds = ds.drop_vars(["grad"])

# rename other variables
ds = ds.rename({"t": "T", "tp": "PP"})

# assign dataset name
ds.attrs["dataset"] = "IE_MERA_FC3hr_3_day"

# reassign CRS
ds.rio.write_crs(data_crs, inplace=True)

# ## Visualise

# Moorepark, Fermoy met station coords
LON, LAT = -8.26389, 52.16389

# transform coordinates from lon/lat to Lambert Conformal Conic
XLON, YLAT = cplt.projection_lambert_conformal.transform_point(
    x=LON, y=LAT, src_crs=ccrs.PlateCarree()
)


def plot_map(data, var, cmap="Spectral_r"):
    """
    Helper function for plotting maps
    """

    plt.figure(figsize=(9, 7))
    ax = plt.axes(projection=cplt.projection_lambert_conformal)
    data.isel(time=120)[var].plot.contourf(
        ax=ax,
        robust=True,
        x="x",
        y="y",
        levels=10,
        transform=cplt.projection_lambert_conformal,
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


def plot_ts(data, var):
    """
    Helper function for plotting time series
    """

    plt.figure(figsize=(12, 4))
    data_ts = data.sel({"x": XLON, "y": YLAT}, method="nearest")
    data_ts = data_ts.sel(time=slice("1989", "1991"))
    plt.plot(data_ts["time"], data_ts[var])
    plt.title(
        data[var].attrs["long_name"] + " [" + data[var].attrs["units"] + "]"
    )
    plt.tight_layout()
    plt.show()


for var in ds.data_vars:
    plot_map(ds, var, cplt.colormap_configs(var))

for var in ds.data_vars:
    plot_ts(ds, var)

# box plots
ds_box = ds.sel({"x": XLON, "y": YLAT}, method="nearest").sel(
    time=slice("1981", "2005")
)

ds_df = pd.DataFrame({"time": ds_box["time"]})
for var in ds_box.data_vars:
    ds_df[var] = ds_box[var]
ds_df.set_index("time", inplace=True)

fig, axs = plt.subplots(2, 2, figsize=(12, 4))
for ax, var in zip(axs.flat, ds_box.data_vars):
    ds_df.plot.box(
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
        f"{ds_box[var].attrs['long_name']} [{ds_box[var].attrs['units']}]"
    )
    ax.set(yticklabels=[])
plt.tight_layout()
plt.show()

# ## Extend data to spin-up year

# copy 1981 data to 1980
ds_interp = ds.interp(
    time=pd.date_range("1980-01-01", "1980-12-31", freq="D"),
    kwargs={"fill_value": None},
)

ds_interp.rio.write_crs(data_crs, inplace=True)

# merge spin-up year with first two years of the main data
ds_interp = xr.combine_by_coords(
    [ds_interp, ds.sel(time=slice("1981", "1982"))]
)

ds_interp

# check value for the first day of the first year
ds.sel({"x": XLON, "y": YLAT}, method="nearest").isel(time=0)["T"].values

# check first value of spin-up year - should be nan
ds_interp.sel({"x": XLON, "y": YLAT}, method="nearest").isel(time=0)[
    "T"
].values

# shift first year of the main data to the spin-up year
ds_interp = ds_interp.shift(time=-ds_interp.sel(time="1980").dims["time"])

# check value for the first day of the first year
ds_interp.sel({"x": XLON, "y": YLAT}, method="nearest").isel(time=0)[
    "T"
].values

# keep only spin-up year
ds_interp = ds_interp.sel(time="1980")

# merge with main dataset
ds = xr.combine_by_coords([ds, ds_interp])

ds.rio.write_crs(data_crs, inplace=True)

# visualise
# spin-up year and first year should be identical
ds_interp = ds.sel({"x": XLON, "y": YLAT}, method="nearest").sel(
    time=slice("1980", "1982")
)
plt.figure(figsize=(12, 4))
plt.plot(ds_interp["time"], ds_interp["T"])
plt.title(f"{ds['T'].attrs['long_name']} [{ds['T'].attrs['units']}]")
plt.tight_layout()
plt.show()
