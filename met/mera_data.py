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
import glob
from datetime import date, datetime, timezone
import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.units as munits
import numpy as np
import pooch
import xarray as xr
import climag.plot_configs as cplt

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
# Cork Airport met station coords
LON = -8.48611
LAT = 51.84722

# %%
# Ireland boundary (derived from NUTS 2021)
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")

# %%
DATA_DIR = os.path.join("data", "MERA", "sample")
os.makedirs(DATA_DIR, exist_ok=True)

# %%
URL = "https://www.met.ie/downloads/MERA_PRODYEAR_2015_06_11_105_2_0_FC3hr.grb"
FILE_NAME = "MERA_PRODYEAR_2015_06_11_105_2_0_FC3hr"

# %%
# download data if necessary
# sample GRIB data; 2 m temperature; 3-h forecasts
if not os.path.isfile(os.path.join(DATA_DIR, FILE_NAME)):
    pooch.retrieve(
        url=URL,
        known_hash=None,
        fname=f"{FILE_NAME}.grb",
        path=DATA_DIR
    )

    with open(
        os.path.join(DATA_DIR, f"{FILE_NAME[:-4]}.txt"), "w", encoding="utf-8"
    ) as outfile:
        outfile.write(
            f"Data downloaded on: {datetime.now(tz=timezone.utc)}\n"
            f"Download URL: {URL}"
        )

# %%
# path to example data file
BASE_FILE_NAME = os.path.join(DATA_DIR, FILE_NAME)

# %% [markdown]
# ## Read original GRIB data

# %%
data = xr.open_dataset(
    f"{BASE_FILE_NAME}.grb", decode_coords="all", chunks="auto"
)

# %%
data

# %%
# save variable attributes
t_attrs = data["t"].attrs

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
(data["t"][0][0] - 273.15).plot(
    robust=True, cmap="Spectral_r", levels=11,
    cbar_kwargs=dict(label="Temperature [°C]")
)
plt.tight_layout()
plt.xlabel(None)
plt.ylabel(None)
plt.title(f"time={data['t'][0][0]['time'].values}")
plt.show()

# %%
plt.figure(figsize=(9, 7))
(data["t"][0][0] - 273.15).plot(
    robust=True, cmap="Spectral_r", x="longitude", y="latitude",
    cbar_kwargs=dict(label="Temperature [°C]"), levels=11
)
plt.xlabel(None)
plt.ylabel(None)
plt.title(f"time={data['t'][0][0]['time'].values}")
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

# %%
# reassign attributes and rename variables
data["var11"].attrs = t_attrs
data = data.rename({"var11": "t"})

# %%
data

# %% [markdown]
# ## Plots

# %%
plt.figure(figsize=(9, 7))
(data["t"][0][0] - 273.15).plot(
    robust=True, cmap="Spectral_r", levels=11,
    cbar_kwargs=dict(label="Temperature [°C]")
)
plt.xlabel(None)
plt.ylabel(None)
plt.title(f"time={data['t'][0][0]['time'].values}")
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
(data["t"][0][0] - 273.15).plot(
    ax=ax, robust=True, cmap="Spectral_r", x="x", y="y", levels=11,
    transform=lambert_conformal, cbar_kwargs=dict(label="Temperature [°C]")
)
ax.gridlines(
    draw_labels=dict(bottom="x", left="y"),
    color="lightslategrey",
    linewidth=.5,
    x_inline=False,
    y_inline=False
)
ax.coastlines(resolution="10m", color="darkslategrey", linewidth=.75)
plt.title(f"time={data['t'][0][0]['time'].values}")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Clip to boundary of Ireland

# %%
data_ie = data.rio.clip(ie.buffer(1).to_crs(data_crs))

# %%
data_ie

# %%
plt.figure(figsize=(9, 7))
ax = plt.axes(projection=cplt.plot_projection)
(data_ie["t"][0][0] - 273.15).plot(
    ax=ax, robust=True, cmap="Spectral_r", x="x", y="y", levels=8,
    transform=lambert_conformal, cbar_kwargs=dict(label="Temperature [°C]")
)
ax.gridlines(
    draw_labels=dict(bottom="x", left="y"),
    color="lightslategrey",
    linewidth=.5,
    x_inline=False,
    y_inline=False
)
ax.coastlines(resolution="10m", color="darkslategrey", linewidth=.75)
plt.title(f"time={data_ie['t'][0][0]['time'].values}")
plt.xlim(-1.75, 1.5)
plt.ylim(-2.05, 2.05)
plt.tight_layout()
plt.show()

# %%
# find number of grid cells with data
len(
    data_ie["t"][0][0].values.flatten()[
        np.isfinite(data_ie["t"][0][0].values.flatten())
    ]
)

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
plt.plot(data_ts["time"], (data_ts["t"] - 273.15))
plt.ylabel("Temperature [°C]")
plt.title(f"lon={LON}, lat={LAT}")
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
fig = (data_sub["t"] - 273.15).plot(
    x="x", y="y", col="time", col_wrap=5, transform=lambert_conformal,
    cmap="Spectral_r", cbar_kwargs=dict(aspect=50, label="Temperature [°C]"),
    robust=True, subplot_kws=dict(projection=cplt.plot_projection),
    levels=13
)

y_ticks = [0, 5, 10, 15, 20, 25]
x_ticks = [25, 26, 27, 28, 29]

for i, ax in enumerate(fig.axs.flat):
    ie.to_crs(cplt.plot_projection).boundary.plot(
        ax=ax, color="darkslategrey", linewidth=.5
    )
    ax.set_xlim(-1.9, 1.6)
    ax.set_ylim(-2.1, 2.1)
    if i in y_ticks:
        ax.gridlines(
            draw_labels=["y", "left"],
            ylocs=range(-90, 90, 1),
            color="None",
            linewidth=.5,
            x_inline=False,
            y_inline=False
        )
    if i in x_ticks:
        ax.gridlines(
            draw_labels=["x", "bottom"],
            xlocs=range(-180, 180, 2),
            color="None",
            linewidth=.5,
            x_inline=False,
            y_inline=False
        )

plt.show()

# %% [markdown]
# ## 1981 ANALYSIS data - 2 m temperature

# %%
data = xr.open_mfdataset(
    glob.glob(
        os.path.join("data", "MERA", "11", "*", "*", "*", "*ANALYSIS")
    ),
    chunks="auto",
    decode_coords="all",
    engine="cfgrib"
)

# %%
data

# %%
# copy variable attributes
t_attrs = data["t"].attrs

# %%
# convert 0/360 deg to -180/180 deg lon
long_attrs = data.longitude.attrs
data = data.assign_coords(longitude=(((data.longitude + 180) % 360) - 180))
# reassign attributes
data.longitude.attrs = long_attrs

# %% [markdown]
# ### Convert to NetCDF

# %%
for f in glob.glob(
    os.path.join("data", "MERA", "11", "*", "*", "*", "*ANALYSIS")
):
    os.system(f"cdo -f nc copy {f} {f}.nc")

# %% [markdown]
# ### Read data

# %%
data = xr.open_mfdataset(
    glob.glob(
        os.path.join("data", "MERA", "11", "*", "*", "*", "*ANALYSIS.nc")
    ),
    chunks="auto",
    decode_coords="all"
)

# %%
data

# %%
data.rio.crs

# %%
# copy CRS
data_crs = data.rio.crs

# %%
# reassign attributes and rename variables
data["var11"].attrs = t_attrs
data = data.rename({"var11": "t"})

# %%
plt.figure(figsize=(9, 7))
ax = plt.axes(projection=lambert_conformal)
(data["t"][1400][0] - 273.15).plot(
    ax=ax, robust=True, cmap="Spectral_r", x="x", y="y", levels=10,
    transform=lambert_conformal, cbar_kwargs=dict(label="Temperature [°C]")
)
ax.gridlines(
    draw_labels=dict(bottom="x", left="y"),
    color="lightslategrey",
    linewidth=.5,
    x_inline=False,
    y_inline=False
)
ax.coastlines(resolution="10m", color="darkslategrey", linewidth=.75)
plt.title(f"time={data['t'][1400][0]['time'].values}")
plt.tight_layout()
plt.show()

# %% [markdown]
# ### Clip to boundary of Ireland

# %%
data_ie = data.rio.clip(ie.buffer(1).to_crs(data_crs))

# %%
data_ie

# %%
plt.figure(figsize=(9, 7))
ax = plt.axes(projection=cplt.plot_projection)
(data_ie["t"][1400][0] - 273.15).plot(
    ax=ax, robust=True, cmap="Spectral_r", x="x", y="y", levels=6,
    transform=lambert_conformal, cbar_kwargs=dict(label="Temperature [°C]")
)
ax.gridlines(
    draw_labels=dict(bottom="x", left="y"),
    color="lightslategrey",
    linewidth=.5,
    x_inline=False,
    y_inline=False
)
ax.coastlines(resolution="10m", color="darkslategrey", linewidth=.75)
plt.title(f"time={data_ie['t'][1400][0]['time'].values}")
plt.xlim(-1.75, 1.5)
plt.ylim(-2.05, 2.05)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### Time series for a point (Cork Airport met station)

# %%
# extract data for the nearest grid cell to the point
data_ts = data.sel(dict(x=XLON, y=YLAT), method="nearest")

# %%
data_ts

# %%
plt.figure(figsize=(12, 4))
plt.plot(data_ts["time"], (data_ts["t"] - 273.15))
plt.ylabel("Temperature [°C]")
plt.title(f"lon={LON}, lat={LAT}")
plt.tight_layout()
plt.show()

# %% [markdown]
# ### Facet plots

# %%
# subset data at T=12:00, d=15
time_list = []
for time in data_ie["time"].values:
    if "15T12:00" in str(time):
        time_list.append(time)

# %%
data_sub = data_ie.sel(time=time_list)

# %%
data_sub

# %%
fig = (data_sub["t"] - 273.15).plot(
    x="x", y="y", col="time", col_wrap=4, transform=lambert_conformal,
    cmap="Spectral_r", cbar_kwargs=dict(aspect=25, label="Temperature [°C]"),
    robust=True, subplot_kws=dict(projection=cplt.plot_projection),
    levels=20
)

y_ticks = [0, 4, 8]  # index of subplots with y tick labels
x_ticks = [8, 9, 10, 11]  # index of subplots with x tick labels

for i, ax in enumerate(fig.axs.flat):
    ie.to_crs(cplt.plot_projection).boundary.plot(
        ax=ax, color="darkslategrey", linewidth=.5
    )
    ax.set_xlim(-1.9, 1.6)
    ax.set_ylim(-2.1, 2.1)
    if i in y_ticks:
        ax.gridlines(
            draw_labels=["y", "left"],
            ylocs=range(-90, 90, 1),
            color="None",
            linewidth=.5,
            x_inline=False,
            y_inline=False
        )
    if i in x_ticks:
        ax.gridlines(
            draw_labels=["x", "bottom"],
            xlocs=range(-180, 180, 2),
            color="None",
            linewidth=.5,
            x_inline=False,
            y_inline=False
        )

plt.show()
