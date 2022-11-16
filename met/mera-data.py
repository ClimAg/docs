# %% [markdown]
# # Met Éireann Reanalysis
#
# <https://www.met.ie/climate/available-data/mera>
#
# Issues:
#
# - 0/360 longitude coordinates instead of -180/180
#   - data spans both negative and positive longitudes
# - projection issues
# - lon/lat are multidimensional coordinates (y, x)
#   - data with two-dimensional coordinates cannot be indexed or selected
#   - x and y correspond to the index of the cells and not in Lambert Conformal Conic
#
# Solution:
#
# - use CDO to convert the GRIB file to NetCDF first
#   - projection info is parsed and can be read by Xarray
#   - one-dimensional coordinates in Lambert Conformal Conic projection
#   - data can now be indexed or selected spatially and temporally using Xarray
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
from datetime import datetime, timezone
import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib.pyplot as plt
import xarray as xr

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
# Cork Airport met station coords
LON = -8.48611
LAT = 51.84722

# %%
# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_Ireland_ITM")

# %%
# example data file - 2 m temperature
BASE_FILE_NAME = os.path.join(
    "data", "met", "MERA", "MERA_PRODYEAR_2015_06_11_105_2_0_FC3hr"
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
# convert 360 deg to 180 deg lon
long_attrs = data.longitude.attrs
data = data.assign_coords(longitude=(((data.longitude + 180) % 360) - 180))
# reassign attributes
data.longitude.attrs = long_attrs

# %%
data

# %% [markdown]
# ### Plot

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

# %%
plt.figure(figsize=(9, 7))
ax = plt.axes(projection=ccrs.AlbersEqualArea())
data["t"][0][0].plot(
    ax=ax, robust=True, levels=15, cmap="Spectral_r",
    transform=ccrs.PlateCarree(), x="longitude", y="latitude"
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
# define Lambert Conformal Conic projection for plots
plot_transform = ccrs.LambertConformal(
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
plot_transform

# %%
plt.figure(figsize=(9, 7))
ax = plt.axes(projection=plot_transform)
data["var11"][0][0].plot(
    ax=ax, robust=True, levels=15, cmap="Spectral_r",
    x="x", y="y", transform=plot_transform,
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
ax = plt.axes(projection=plot_transform)
data_ie["var11"][0][0].plot(
    ax=ax, robust=True, levels=15, cmap="Spectral_r",
    x="x", y="y", transform=plot_transform,
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
XLON, YLAT = plot_transform.transform_point(
    x=LON, y=LAT, src_crs=ccrs.PlateCarree()
)

# %%
XLON, YLAT

# %%
# find nearest grid cell to the point
data_ts = data.sel({"x": XLON, "y": YLAT}, method="nearest")

# %%
data_ts

# %%
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
    levels=15, transform=plot_transform,
    subplot_kws=dict(projection=plot_transform)
)

for i, ax in enumerate(fig.axes.flat):
    ie.to_crs(plot_transform).boundary.plot(
        ax=ax, color="darkslategrey", linewidth=.5
    )

plt.show()
