# %% [markdown]
# # Met Éireann Reanalysis
#
# <https://www.met.ie/climate/available-data/mera>
#
# Issues:
#
# - data uses 0/360 longitude coordinates instead of -180/180
#   - data spans both negative and positive longitudes
# - projection information is not parsed when the data is read
# - lon/lat are multidimensional coordinates (y, x)
#   - data with two-dimensional coordinates cannot be spatially selected (e.g.
#     extracting data for a certain point, or clipping with a geometry)
#   - x and y correspond to the index of the cells and are not coordinates in
#     Lambert Conformal Conic projection
#
# Solution:
#
# - use CDO to convert the GRIB file to NetCDF first
#   - projection info is parsed and can be read by Xarray
#   - one-dimensional coordinates in Lambert Conformal Conic projection
#   - data can now be indexed or selected both spatially and temporally using
#     Xarray
#   - some metadata are lost (e.g. variable name and attributes) but these can
#     be reassigned manually
#   - this method combines all three time steps in the example data (data needs
#     to be split prior to conversion to avoid this)
#
# Relevant links:
#
# - <https://docs.xarray.dev/en/stable/examples/multidimensional-coords.html>
# - <https://docs.xarray.dev/en/stable/examples/ERA5-GRIB-example.html>
# - <https://scitools.org.uk/cartopy/docs/latest/reference/projections.html>
# - <https://confluence.ecmwf.int/display/OIFS/How+to+convert+GRIB+to+netCDF>
# - <https://github.com/corteva/rioxarray/issues/135>
# - <https://docs.xarray.dev/en/stable/generated/xarray.DataArray.assign_coords.html>
#
# Example data used:
# <https://www.met.ie/downloads/MERA_PRODYEAR_2015_06_11_105_2_0_FC3hr.grb>
#
# Requirements:
#
# - CDO
# - Python 3.10
#   - rioxarray
#   - geopandas
#   - dask
#   - cartopy
#   - matplotlib
#   - nc-time-axis

# %%
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

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DRIVE = "/run/media/nms/Elements"

# %%
# Cork Airport met station coords
LON = -8.48611
LAT = 51.84722

# %%
# Ireland boundary (derived from NUTS 2021)
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_Ireland_ITM")

# %%
DATA_DIR = os.path.join(DATA_DRIVE, "MERA", "sample")
os.makedirs(DATA_DIR, exist_ok=True)

# %%
# download sample GRIB data; 2 m temperature; 3-h forecasts
URL = "https://www.met.ie/downloads/MERA_PRODYEAR_2015_06_11_105_2_0_FC3hr.grb"
KNOWN_HASH = "3106063013265c1b1e9f535938aac7e391e2926b0df9ec15e2ed97e7fd0b565f"

pooch.retrieve(
    url=URL,
    known_hash=KNOWN_HASH,
    fname="MERA_PRODYEAR_2015_06_11_105_2_0_FC3hr.grb",
    path=DATA_DIR,
    progressbar=True
)

# %%
# path to example data file
BASE_FILE_NAME = os.path.join(
    DATA_DIR, "MERA_PRODYEAR_2015_06_11_105_2_0_FC3hr"
)

# %% [markdown]
# ## Read original GRIB data

# %%
data = xr.open_dataset(
    f"{BASE_FILE_NAME}.grb", decode_coords="all", chunks="auto"
)

# %%
data

# %%
# convert 0/360 deg to -180/180 deg lon
long_attrs = data.longitude.attrs
data = data.assign_coords(longitude=(((data.longitude + 180) % 360) - 180))
# reassign attributes
data.longitude.attrs = long_attrs

# %% [markdown]
# ### Plots

# %%
plt.figure(figsize=(9, 7))
data["t"][0][0].plot(robust=True, levels=15, cmap="Spectral_r")
plt.tight_layout()
plt.show()

# %%
plt.figure(figsize=(9, 7))
data["t"][0][0].plot(
    robust=True, levels=15, cmap="Spectral_r", x="longitude", y="latitude"
)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Convert GRIB to NetCDF using CDO

# %%
os.system(f"cdo -f nc copy {BASE_FILE_NAME}.grb {BASE_FILE_NAME}.nc")

# %% [markdown]
# ## Read data

# %%
data = xr.open_dataset(
    f"{BASE_FILE_NAME}.nc", decode_coords="all", chunks="auto"
)

# %%
data

# %%
data.rio.crs

# %%
# save CRS info
data_crs = data.rio.crs

# %% [markdown]
# ## Plots

# %%
plt.figure(figsize=(9, 7))
data["var11"][0][0].plot(
    robust=True, levels=15, cmap="Spectral_r",
    cbar_kwargs=dict(label="Temperature [K]")
)
plt.tight_layout()
plt.show()

# %%
# define Lambert Conformal Conic projection for plots and transformations
# using metadata
lambert_conformal = ccrs.LambertConformal(
    false_easting=data["Lambert_Conformal"].attrs["false_easting"],
    false_northing=data["Lambert_Conformal"].attrs["false_northing"],
    standard_parallels=[data["Lambert_Conformal"].attrs["standard_parallel"]],
    central_longitude=(
        data["Lambert_Conformal"].attrs["longitude_of_central_meridian"]
    ),
    central_latitude=(
        data["Lambert_Conformal"].attrs["latitude_of_projection_origin"]
    )
)

# %%
lambert_conformal

# %%
plt.figure(figsize=(9, 7))
ax = plt.axes(projection=lambert_conformal)
data["var11"][0][0].plot(
    ax=ax, robust=True, levels=15, cmap="Spectral_r",
    x="x", y="y", transform=lambert_conformal,
    cbar_kwargs=dict(label="Temperature [K]")
)
ax.gridlines(
    draw_labels=dict(bottom="x", left="y"),
    color="lightslategrey",
    linewidth=.5,
    x_inline=False,
    y_inline=False
)
ax.coastlines(resolution="10m", color="darkslategrey", linewidth=.75)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Clip to boundary of Ireland

# %%
data_ie = data.rio.clip(ie.buffer(2500).to_crs(data_crs))

# %%
data_ie

# %%
plt.figure(figsize=(9, 7))
data_ie["var11"][0][0].plot(
    robust=True, levels=15, cmap="Spectral_r",
    cbar_kwargs=dict(label="Temperature [K]")
)
plt.tight_layout()
plt.show()

# %%
plt.figure(figsize=(9, 7))
ax = plt.axes(projection=lambert_conformal)
data_ie["var11"][0][0].plot(
    ax=ax, robust=True, levels=15, cmap="Spectral_r",
    x="x", y="y", transform=lambert_conformal,
    cbar_kwargs=dict(label="Temperature [K]")
)
ax.gridlines(
    draw_labels=dict(bottom="x", left="y"),
    color="lightslategrey",
    linewidth=.5,
    x_inline=False,
    y_inline=False
)
ax.coastlines(resolution="10m", color="darkslategrey", linewidth=.75)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Time series for a point (Cork Airport met station)

# %%
# transform coordinates from lon/lat to Lambert Conformal Conic
XLON, YLAT = lambert_conformal.transform_point(
    x=LON, y=LAT, src_crs=ccrs.PlateCarree()
)

# %%
XLON, YLAT

# %%
# extract data for the nearest grid cell to the point
data_ts = data.sel(dict(x=XLON, y=YLAT), method="nearest")

# %%
data_ts

# %%
converter = mdates.ConciseDateConverter()
munits.registry[np.datetime64] = converter
munits.registry[date] = converter
munits.registry[datetime] = converter

plt.figure(figsize=(12, 4))
plt.plot(data_ts["time"], data_ts["var11"])
plt.ylabel("Temperature [K]")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Facet plots

# %%
# subset data at T=12:00
time_list = []
for time in data_ie["time"].values:
    if "12:00" in str(time):
        time_list.append(time)

# %%
data_sub = data_ie.sel(time=time_list)

# %%
data_sub

# %%
fig = data_sub["var11"].plot(
    x="x", y="y", col="time", col_wrap=5, cmap="Spectral_r",
    robust=True, cbar_kwargs=dict(aspect=40, label="Temperature [K]"),
    levels=15, transform=lambert_conformal,
    subplot_kws=dict(projection=lambert_conformal)
)

for ax in fig.axes.flat:
    ie.to_crs(lambert_conformal).boundary.plot(
        ax=ax, color="darkslategrey", linewidth=.5
    )

plt.show()
