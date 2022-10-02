# %% [markdown]
# # Subset EURO-CORDEX data for Ireland

# %%
# import libraries
import os
from datetime import datetime, timezone
import geopandas as gpd
import intake
import matplotlib.pyplot as plt
import xarray as xr
import climag.plot_configs as cplt

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR_BASE = os.path.join("data", "eurocordex")

# %%
# directory to store outputs
DATA_DIR = os.path.join(DATA_DIR_BASE, "IE")
os.makedirs(DATA_DIR, exist_ok=True)

# %%
# Cork Airport met station coords
LON = -8.48611
LAT = 51.84722

# %%
# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="OS_IE_Ireland_ITM")

# %%
MODVEGE_DIR = os.path.join("data", "grass-growth", "modvege")

# %% [markdown]
# ## Reading the local catalogue

# %%
# JSON_FILE_PATH = (
#     "https://raw.githubusercontent.com/ClimAg/data/main/eurocordex/"
#     "eurocordex_eur11_local.json"
# )
JSON_FILE_PATH = os.path.join(
    DATA_DIR_BASE, "eurocordex_eur11_local_disk.json"
)

# %%
cordex_eur11_cat = intake.open_esm_datastore(JSON_FILE_PATH)

# %%
list(cordex_eur11_cat)

# %%
cordex_eur11_cat

# %%
cordex_eur11_cat.df.shape

# %%
cordex_eur11_cat.df.head()

# %% [markdown]
# ## Read a subset (precipitation)

# %%
# filter data subset
cordex_eur11 = cordex_eur11_cat.search(
    experiment_id="rcp85",
    variable_id="pr",
    institute_id="SMHI"
)

# %%
cordex_eur11

# %%
cordex_eur11.df

# %%
data = xr.open_mfdataset(
    list(cordex_eur11.df["uri"]),
    chunks="auto",
    decode_coords="all"
)
# data = cordex_eur11.to_dataset_dict(
#     xarray_open_kwargs=dict(chunks=True, decode_coords="all")
# )

# %%
data

# %%
# # read one of the data files to extract CRS info
# data_ec = xr.open_dataset(
#     cordex_eur11.df["uri"][0], decode_coords="all", chunks=True
# )

# data.rio.write_crs(data_ec.rio.crs, inplace=True)

# data = data.set_coords(("time_bnds"))

# del data["pr"].attrs["grid_mapping"]

data.rio.crs

# %% [markdown]
# ### Ireland subset

# %%
# clip to Ireland's bounding box with a 10 km buffer
data = data.rio.clip(ie.envelope.buffer(10000).to_crs(data.rio.crs))

# %%
data

# %%
# export to NetCDF
FILE_NAME = cplt.ie_ncfile_name(data)

# %%
data.to_netcdf(os.path.join(DATA_DIR, FILE_NAME))

# %% [markdown]
# #### Time subset

# %%
data_ie = data.isel(time=50)

# %%
data_ie

# %%
plot_transform = cplt.rotated_pole_transform(data_ie)
plot_data = data_ie["pr"] * 60 * 60 * 24  # convert to mm/day
cbar_label = data_ie["pr"].attrs["long_name"] + " [mm/day]"  # colorbar label

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

ax.set_title(cplt.cordex_plot_title(data_ie))  # set plot title

plt.show()

# %% [markdown]
# #### Point subset

# %%
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

# %%
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
data_ie

# %%
plt.figure(figsize=(12, 4))
plt.plot(data_ie["time"], data_ie["pr"] * 60 * 60 * 24)
plt.xlabel(data_ie["time"].attrs["standard_name"])
plt.ylabel(data_ie["pr"].attrs["long_name"] + " [mm/day]")
plt.title(cplt.cordex_plot_title(data_ie, lon=LON, lat=LAT))
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Read a subset (evapotranspiration)

# %%
# filter data subset
cordex_eur11 = cordex_eur11_cat.search(
    experiment_id="rcp85",
    variable_id="evspsblpot",
    institute_id="SMHI"
)

# %%
cordex_eur11

# %%
cordex_eur11.df

# %%
data = xr.open_mfdataset(
    list(cordex_eur11.df["uri"]),
    chunks="auto",
    decode_coords="all"
)

# %%
data

# %% [markdown]
# ### Ireland subset

# %%
# clip to Ireland's bounding box with a 10 km buffer
data = data.rio.clip(ie.envelope.buffer(10000).to_crs(data.rio.crs))

# %%
data

# %%
# export to NetCDF
FILE_NAME = cplt.ie_ncfile_name(data)

# %%
data.to_netcdf(os.path.join(DATA_DIR, FILE_NAME))

# %% [markdown]
# #### Time subset

# %%
data_ie = data.isel(time=50)

# %%
data_ie

# %%
plot_transform = cplt.rotated_pole_transform(data_ie)
plot_data = data_ie["evspsblpot"] * 60 * 60 * 24  # convert to mm/day
cbar_label = data_ie["evspsblpot"].attrs["long_name"] + " [mm/day]"

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

ax.set_title(cplt.cordex_plot_title(data_ie))  # set plot title

plt.show()

# %% [markdown]
# #### Point subset

# %%
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

# %%
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
plt.figure(figsize=(12, 4))
plt.plot(data_ie["time"], data_ie["evspsblpot"] * 60 * 60 * 24)
plt.xlabel(data_ie["time"].attrs["standard_name"])
plt.ylabel(data_ie["evspsblpot"].attrs["long_name"] + " [mm/day]")
plt.title(cplt.cordex_plot_title(data_ie, lon=LON, lat=LAT))
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Read a subset (temperature)

# %%
# filter data subset
cordex_eur11 = cordex_eur11_cat.search(
    experiment_id="rcp85",
    variable_id="tas",
    institute_id="SMHI"
)

# %%
cordex_eur11

# %%
cordex_eur11.df

# %%
data = xr.open_mfdataset(
    list(cordex_eur11.df["uri"]),
    chunks="auto",
    decode_coords="all"
)

# %%
data

# %% [markdown]
# ### Ireland subset

# %%
# clip to Ireland's bounding box with a 10 km buffer
data = data.rio.clip(ie.envelope.buffer(10000).to_crs(data.rio.crs))

# %%
data

# %%
# export to NetCDF
FILE_NAME = cplt.ie_ncfile_name(data)

# %%
data.to_netcdf(os.path.join(DATA_DIR, FILE_NAME))

# %% [markdown]
# #### Time subset

# %%
data_ie = data.isel(time=50)

# %%
data_ie

# %%
plot_transform = cplt.rotated_pole_transform(data_ie)
plot_data = data_ie["tas"] - 273.15  # convert to deg C
cbar_label = data_ie["tas"].attrs["long_name"] + " [°C]"

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

ax.set_title(cplt.cordex_plot_title(data_ie))  # set plot title

plt.show()

# %% [markdown]
# #### Point subset

# %%
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

# %%
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
plt.figure(figsize=(12, 4))
plt.plot(data_ie["time"], data_ie["tas"] * 60 * 60 * 24)
plt.xlabel(data_ie["time"].attrs["standard_name"])
plt.ylabel(data_ie["tas"].attrs["long_name"] + " [°C]")
plt.title(cplt.cordex_plot_title(data_ie, lon=LON, lat=LAT))
plt.tight_layout()
plt.show()
