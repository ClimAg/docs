# %% [markdown]
# # EURO-CORDEX data from NC files

# %%
# import libraries
import os
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
import xarray as xr
import climag.plot_configs as cplt

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR_BASE = os.path.join("data", "eurocordex", "DMI")

# %%
# Cork Airport met station coords
LON = -8.48611
LAT = 51.84722

# %%
# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="Boundary_IE_NUTS_ITM")

# %% [markdown]
# ## tasmin

# %%
FILE_PATH = os.path.join(
    DATA_DIR_BASE,
    "historical",
    "mon",
    "tasmin_EUR-11_NCC-NorESM1-M_historical_r1i1p1_" +
    "DMI-HIRHAM5_v3_mon_200101-200512.nc"
)

# %%
data_ec = xr.open_dataset(FILE_PATH, decode_coords="all", chunks=True)

# %%
data_ec

# %%
data_ec.rio.crs

# %%
# extract time series for Cork Airport
cds = cplt.rotated_pole_point(data_ec, lon=LON, lat=LAT)
data_ca = data_ec.sel({"rlat": cds[1], "rlon": cds[0]}, method="nearest")

# %%
data_ca

# %%
plt.figure(figsize=(12, 4))
plt.plot(
    data_ca["time"], data_ca[list(data_ca.keys())[0]] - 273.15, marker="o"
)
plt.xlabel(data_ca["time"].attrs["standard_name"])
plt.ylabel(data_ca[list(data_ca.keys())[0]].attrs["long_name"] + " [°C]")
plt.title(cplt.cordex_plot_title(data_ca, lon=LON, lat=LAT))
plt.tight_layout()
plt.show()

# %%
# extract data for a given time
data_50 = data_ec.isel(time=50)

# %%
data_50

# %%
plot_transform = cplt.rotated_pole_transform(data_50)
data_var = data_50[list(data_50.keys())[0]]  # extract variable name
plot_data = data_var - 273.15  # convert to deg C
cbar_label = data_var.attrs["long_name"] + " [°C]"  # colorbar label

plt.figure(figsize=(20, 10))
ax = plt.axes(projection=plot_transform)

# specify gridline spacing and labels
ax.gridlines(
    draw_labels=True,
    xlocs=range(-180, 180, 10),
    ylocs=range(-90, 90, 5),
    color="lightslategrey",
    linewidth=.5
)

# plot data for the variable
plot_data.plot(
    ax=ax,
    cmap="Spectral_r",
    transform=plot_transform,
    x="rlon",
    y="rlat",
    cbar_kwargs=dict(label=cbar_label)
)

# add boundaries
ax.coastlines(resolution="50m", color="darkslategrey", linewidth=.5)

ax.set_title(cplt.cordex_plot_title(data_50))  # set plot title

plt.show()

# %%
# clip to Ireland's bounding box with a 10 km buffer
data_ie = data_50.rio.clip(ie.envelope.buffer(10000).to_crs(data_50.rio.crs))

# %%
plot_transform = cplt.rotated_pole_transform(data_ie)
data_var = data_ie[list(data_ie.keys())[0]]  # extract variable name
plot_data = data_var - 273.15  # convert to deg C
cbar_label = data_var.attrs["long_name"] + " [°C]"  # colorbar label

plt.figure(figsize=(20, 10))
ax = plt.axes(projection=plot_transform)

# specify gridline spacing and labels
ax.gridlines(
    draw_labels=True,
    xlocs=range(-180, 180, 2),
    ylocs=range(-90, 90, 1),
    color="lightslategrey",
    linewidth=.5
)

# plot data for the variable
plot_data.plot(
    ax=ax,
    cmap="Spectral_r",
    transform=plot_transform,
    x="rlon",
    y="rlat",
    cbar_kwargs=dict(label=cbar_label)
)

# add boundaries
ax.coastlines(resolution="10m", color="darkslategrey", linewidth=.75)

# Cork Airport marker
# plt.scatter(cds[0], cds[1], s=100, c="darkslategrey", marker="*")

ax.set_title(cplt.cordex_plot_title(data_ie))  # set plot title

plt.show()

# %% [markdown]
# ## tasmax

# %%
FILE_PATH = os.path.join(
    DATA_DIR_BASE,
    "historical",
    "mon",
    "tasmax_EUR-11_NCC-NorESM1-M_historical_r1i1p1_" +
    "DMI-HIRHAM5_v3_mon_200101-200512.nc"
)

data_ec = xr.open_dataset(FILE_PATH, decode_coords="all", chunks=True)

cds = cplt.rotated_pole_point(data_ec, lon=LON, lat=LAT)
data_ca = data_ec.sel({"rlat": cds[1], "rlon": cds[0]}, method="nearest")

# %%
plt.figure(figsize=(12, 4))
plt.plot(
    data_ca["time"], data_ca[list(data_ca.keys())[0]] - 273.15, marker="o"
)
plt.xlabel(data_ca["time"].attrs["standard_name"])
plt.ylabel(data_ca[list(data_ca.keys())[0]].attrs["long_name"] + " [°C]")
plt.title(cplt.cordex_plot_title(data_ca, lon=LON, lat=LAT))
plt.tight_layout()
plt.show()

# %%
data_50 = data_ec.isel(time=50)

# %%
plot_transform = cplt.rotated_pole_transform(data_50)
data_var = data_50[list(data_50.keys())[0]]  # extract variable name
plot_data = data_var - 273.15  # convert to deg C
cbar_label = data_var.attrs["long_name"] + " [°C]"  # colorbar label

plt.figure(figsize=(20, 10))
ax = plt.axes(projection=plot_transform)

# specify gridline spacing and labels
ax.gridlines(
    draw_labels=True,
    xlocs=range(-180, 180, 10),
    ylocs=range(-90, 90, 5),
    color="lightslategrey",
    linewidth=.5
)

# plot data for the variable
plot_data.plot(
    ax=ax,
    cmap="Spectral_r",
    transform=plot_transform,
    x="rlon",
    y="rlat",
    cbar_kwargs=dict(label=cbar_label)
)

# add boundaries
ax.coastlines(resolution="50m", color="darkslategrey", linewidth=.5)

ax.set_title(cplt.cordex_plot_title(data_50))  # set plot title

plt.show()

# %%
data_ie = data_50.rio.clip(
    ie.envelope.buffer(10000).to_crs(data_50.rio.crs)
)

# %%
plot_transform = cplt.rotated_pole_transform(data_ie)
data_var = data_ie[list(data_ie.keys())[0]]  # extract variable name
plot_data = data_var - 273.15  # convert to deg C
cbar_label = data_var.attrs["long_name"] + " [°C]"  # colorbar label

plt.figure(figsize=(20, 10))
ax = plt.axes(projection=plot_transform)

# specify gridline spacing and labels
ax.gridlines(
    draw_labels=True,
    xlocs=range(-180, 180, 2),
    ylocs=range(-90, 90, 1),
    color="lightslategrey",
    linewidth=.5
)

# plot data for the variable
plot_data.plot(
    ax=ax,
    cmap="Spectral_r",
    transform=plot_transform,
    x="rlon",
    y="rlat",
    cbar_kwargs=dict(label=cbar_label)
)

# add boundaries
ax.coastlines(resolution="10m", color="darkslategrey", linewidth=.75)

# Cork Airport marker
# plt.scatter(cds[0], cds[1], s=100, c="darkslategrey", marker="*")

ax.set_title(cplt.cordex_plot_title(data_ie))  # set plot title

plt.show()

# %% [markdown]
# ## pr

# %%
FILE_PATH = os.path.join(
    DATA_DIR_BASE,
    "rcp85",
    "mon",
    "pr_EUR-11_NCC-NorESM1-M_rcp85_r1i1p1_" +
    "DMI-HIRHAM5_v3_mon_204101-205012.nc"
)

data_ec = xr.open_dataset(FILE_PATH, decode_coords="all", chunks=True)

cds = cplt.rotated_pole_point(data_ec, lon=LON, lat=LAT)

# %%
data_ca = data_ec.sel({"rlat": cds[1], "rlon": cds[0]}, method="nearest")

# %%
plt.figure(figsize=(12, 4))
plt.plot(
    data_ca["time"],
    data_ca[list(data_ca.keys())[0]] * 60 * 60 * 24,  # convert to mm/day
    marker="o"
)
plt.xlabel(data_ca["time"].attrs["standard_name"])
plt.ylabel(data_ca[list(data_ca.keys())[0]].attrs["long_name"] + " [mm/day]")
plt.title(cplt.cordex_plot_title(data_ca, lon=LON, lat=LAT))
plt.tight_layout()
plt.show()

# %%
data_50 = data_ec.isel(time=50)

# %%
plot_transform = cplt.rotated_pole_transform(data_50)
data_var = data_50[list(data_50.keys())[0]]  # extract variable name
plot_data = data_var * 60 * 60 * 24  # convert to mm/day
cbar_label = data_var.attrs["long_name"] + " [mm/day]"  # colorbar label

plt.figure(figsize=(20, 10))
ax = plt.axes(projection=plot_transform)

# specify gridline spacing and labels
ax.gridlines(
    draw_labels=True,
    xlocs=range(-180, 180, 10),
    ylocs=range(-90, 90, 5),
    color="lightslategrey",
    linewidth=.5
)

# plot data for the variable
plot_data.plot(
    ax=ax,
    cmap="GnBu",
    transform=plot_transform,
    x="rlon",
    y="rlat",
    cbar_kwargs=dict(label=cbar_label)
)

# add boundaries
ax.coastlines(resolution="50m", color="darkslategrey", linewidth=.5)

ax.set_title(cplt.cordex_plot_title(data_50))  # set plot title

plt.show()

# %%
data_ie = data_50.rio.clip(
    ie.envelope.buffer(10000).to_crs(data_50.rio.crs)
)

# %%
plot_transform = cplt.rotated_pole_transform(data_ie)
data_var = data_ie[list(data_ie.keys())[0]]  # extract variable name
plot_data = data_var * 60 * 60 * 24  # convert to mm/day
cbar_label = data_var.attrs["long_name"] + " [mm/day]"  # colorbar label

plt.figure(figsize=(20, 10))
ax = plt.axes(projection=plot_transform)

# specify gridline spacing and labels
ax.gridlines(
    draw_labels=True,
    xlocs=range(-180, 180, 2),
    ylocs=range(-90, 90, 1),
    color="lightslategrey",
    linewidth=.5
)

# plot data for the variable
plot_data.plot(
    ax=ax,
    cmap="GnBu",
    transform=plot_transform,
    x="rlon",
    y="rlat",
    cbar_kwargs=dict(label=cbar_label)
)

# add boundaries
ax.coastlines(resolution="10m", color="darkslategrey", linewidth=.75)

# Cork Airport marker
# plt.scatter(cds[0], cds[1], s=100, c="darkslategrey", marker="*")

ax.set_title(cplt.cordex_plot_title(data_ie))  # set plot title

plt.show()
