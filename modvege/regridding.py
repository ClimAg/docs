#!/usr/bin/env python
# coding: utf-8

import os

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import xesmf as xe

import climag.plot_configs as cplt


def plot_map(data, var, x, y, transform, cmap="Spectral_r", contour=False):
    """
    Helper function for plotting maps
    """

    plt.figure(figsize=(9, 7))
    ax = plt.axes(projection=cplt.plot_projection)
    if contour:
        data.isel(time=180)[var].plot.contourf(
            ax=ax,
            x=x,
            y=y,
            levels=10,
            robust=True,
            transform=transform,
            cmap=cmap,
        )
    else:
        data.isel(time=180)[var].plot(
            ax=ax,
            x=x,
            y=y,
            levels=10,
            robust=True,
            transform=transform,
            cmap=cmap,
        )
    ax.gridlines(
        draw_labels=dict(bottom="x", left="y"),
        color="lightslategrey",
        linewidth=0.5,
        x_inline=False,
        y_inline=False,
    )
    ax.coastlines(resolution="10m", color="darkslategrey", linewidth=0.75)
    ax.set_title(str(data.isel(time=180)["time"].values))
    plt.tight_layout()
    plt.show()


# ## Higher resolution dataset

mera_data = os.path.join(
    "data", "ModVege", "MERA", "modvege_IE_MERA_FC3hr_3_day_1989.nc"
)

mera_data = xr.open_dataset(mera_data, decode_coords="all")

mera_data

plot_map(mera_data, "gro", "x", "y", cplt.lambert_conformal, "YlGn")

mera_data.rio.crs

# reproject to lat/lon degrees
d1 = mera_data.rio.reproject(ccrs.PlateCarree())

# rename dims
d1 = d1.rename({"x": "lon", "y": "lat"})

d1

d1.rio.crs

plot_map(d1, "gro", "lon", "lat", ccrs.PlateCarree(), "YlGn")

# ## Lower resolution data

eurocordex_data = os.path.join(
    "data",
    "ModVege",
    "EURO-CORDEX",
    "historical",
    "EC-EARTH",
    "modvege_IE_EURO-CORDEX_RCA4_EC-EARTH_historical_1989.nc",
)

eurocordex_data = xr.open_dataset(eurocordex_data, decode_coords="all")

eurocordex_data

plot_map(
    eurocordex_data,
    "gro",
    "rlon",
    "rlat",
    ccrs.RotatedPole(pole_longitude=-162.0, pole_latitude=39.25),
    "YlGn",
)

d2 = eurocordex_data.drop(["lat", "lon", "time_bnds"])

d2 = d2.rio.reproject(ccrs.PlateCarree())

# normalise to keep only date in time
d2["time"] = d2.indexes["time"].normalize()

d2

# rename dims
d2 = d2.rename({"x": "lon", "y": "lat"})

d2.rio.crs

d2

plot_map(d2, "gro", "lon", "lat", ccrs.PlateCarree(), "YlGn")

plot_map(
    d2.rio.reproject(cplt.eurocordex_projection),
    "gro",
    "x",
    "y",
    cplt.eurocordex_projection,
    "YlGn",
)

# ## Regridding to a lower resolution

regridder = xe.Regridder(d1, d2, "bilinear")

regridder

d3 = regridder(d1)

d3

d3.rio.crs

plot_map(d3, "gro", "lon", "lat", ccrs.PlateCarree(), "YlGn")

# ### Difference

d4 = d2 - d3

d4

d4.rio.crs

plot_map(d4, "gro", "lon", "lat", ccrs.PlateCarree(), "RdBu_r")

plot_map(d4, "gro", "lon", "lat", ccrs.PlateCarree(), "RdBu_r", contour=True)

# ## Regridding to a higher resolution

regridder = xe.Regridder(d2, d1, "bilinear")

regridder

d3 = regridder(d2)

d3

plot_map(d3, "gro", "lon", "lat", ccrs.PlateCarree(), "YlGn")

# ### Difference

d4 = d3 - d1

d4

plot_map(d4, "gro", "lon", "lat", ccrs.PlateCarree(), "RdBu_r")

plot_map(d4, "gro", "lon", "lat", ccrs.PlateCarree(), "RdBu_r", contour=True)
