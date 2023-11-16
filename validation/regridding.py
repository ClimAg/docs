#!/usr/bin/env python
# coding: utf-8

# # Regridding datasets
#
# Options:
#
# - Interpolating using Xarray
#   - <https://docs.xarray.dev/en/stable/user-guide/interpolation.html>
# - Reproject match using Rioxarray
#   - <https://corteva.github.io/rioxarray/stable/examples/reproject_match.html>
#   - <https://rasterio.readthedocs.io/en/stable/api/rasterio.enums.html#rasterio.enums.Resampling>
# - xESMF's regridder
#   - <https://xesmf.readthedocs.io/en/latest/notebooks/Dataset.html>

import os

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import rasterio as rio
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


# ## Higher resolution observational dataset - MERA

obs = os.path.join(
    "data", "ModVege", "MERA", "modvege_IE_MERA_FC3hr_3_day_1989.nc"
)

obs = xr.open_dataset(obs, decode_coords="all")

# reassign projection
obs.rio.write_crs(cplt.lambert_conformal, inplace=True)

plot_map(obs, "gro", "x", "y", cplt.lambert_conformal, "BrBG")

# ## Lower resolution climate model dataset - EURO-CORDEX

clim = os.path.join(
    "data",
    "ModVege",
    "EURO-CORDEX",
    "historical",
    "EC-EARTH",
    "modvege_IE_EURO-CORDEX_RCA4_EC-EARTH_historical_1989.nc",
)

clim = xr.open_dataset(clim, decode_coords="all")

clim

plot_map(clim, "gro", "rlon", "rlat", cplt.eurocordex_projection, "BrBG")

# ## xESMF's Regridder

# drop unnecessary coordinates and normalise to keep only date in time
clim2 = clim.drop(["lat", "lon", "time_bnds"])
clim2["time"] = clim2.indexes["time"].normalize()

# reproject to lat/lon degrees
obs2 = obs.rio.reproject(ccrs.PlateCarree())
clim2 = clim2.rio.reproject(ccrs.PlateCarree())

# rename dims
obs2 = obs2.rename({"x": "lon", "y": "lat"})
clim2 = clim2.rename({"x": "lon", "y": "lat"})

obs2

clim2

plot_map(obs2, "gro", "lon", "lat", ccrs.PlateCarree(), "BrBG")

plot_map(clim2, "gro", "lon", "lat", ccrs.PlateCarree(), "BrBG")

regridder = xe.Regridder(clim2, obs2, "bilinear")

regridder

clim2 = regridder(clim2)

clim2

plot_map(clim2, "gro", "lon", "lat", ccrs.PlateCarree(), "BrBG")

# ### Difference

diff = clim2 - obs2

diff

plot_map(diff, "gro", "lon", "lat", ccrs.PlateCarree(), "RdBu_r")

plot_map(diff, "gro", "lon", "lat", ccrs.PlateCarree(), "RdBu_r", contour=True)

# ## Xarray's interp_like

# drop unnecessary coordinates and normalise to keep only date in time
clim2 = clim.drop(["lat", "lon", "time_bnds"])
clim2["time"] = clim2.indexes["time"].normalize()

# reproject to observational data's CRS
clim2 = clim2.rio.reproject(cplt.lambert_conformal)
# interpolate
clim2 = clim2.interp_like(obs)

clim2

plot_map(clim2, "gro", "x", "y", cplt.lambert_conformal, "BrBG")

# ### Difference

diff = clim2 - obs

diff

plot_map(diff, "gro", "x", "y", cplt.lambert_conformal, "RdBu_r")

plot_map(diff, "gro", "x", "y", cplt.lambert_conformal, "RdBu_r", contour=True)

# ## Rioxarray's reproject_match

# drop unnecessary coordinates and normalise to keep only date in time
clim2 = clim.drop(["lat", "lon", "time_bnds"])
clim2["time"] = clim2.indexes["time"].normalize()

clim2 = clim2.rename({"rlon": "x", "rlat": "y"})
clim2 = clim2.rio.reproject_match(
    obs, resampling=rio.enums.Resampling.bilinear
)
clim2 = clim2.assign_coords({"x": obs["x"], "y": obs["y"]})

clim2

plot_map(clim2, "gro", "x", "y", cplt.lambert_conformal, "BrBG")

# ### Difference

diff = clim2 - obs

diff

plot_map(diff, "gro", "x", "y", cplt.lambert_conformal, "RdBu_r")

plot_map(diff, "gro", "x", "y", cplt.lambert_conformal, "RdBu_r", contour=True)
