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
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_Ireland_ITM")

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
# ## Read a subset (rcp85)

# %%
cordex_eur11 = cordex_eur11_cat.search(
    experiment_id="rcp85",
    variable_id=["pr", "tas", "evspsblpot"],
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

# %%
data.rio.crs

# %% [markdown]
# ### Ireland subset

# %%
# clip to Ireland's boundary with a 10 km buffer
data = data.rio.clip(ie.buffer(10000).to_crs(data.rio.crs))

# %%
data

# %% [markdown]
# ### Convert units

# %%
for v in data.data_vars:
    var_attrs = data[v].attrs  # extract attributes
    if v == "tas":
        var_attrs["units"] = "°C"  # convert K to deg C
        data[v] = data[v] - 273.15
    else:
        var_attrs["units"] = "mm/day"  # convert kg m-2 s-1 to mm/day
        data[v] = data[v] * 60 * 60 * 24
    data[v].attrs = var_attrs  # reassign attributes

# %%
data

# %% [markdown]
# ### Export data

# %%
# export to NetCDF
FILE_NAME = cplt.ie_cordex_ncfile_name(data)

# %%
data.to_netcdf(os.path.join(DATA_DIR, FILE_NAME))

# %% [markdown]
# #### Time subset

# %%
data_ie = data.isel(time=50)

# %%
data_ie

# %%
for v in data.data_vars:
    cbar_label = (
        data_ie[v].attrs["long_name"] + " [" + data_ie[v].attrs["units"] + "]"
    )  # colorbar label
    if v == "pr":
        cmap = "GnBu"
    elif v == "evspsblpot":
        cmap = "PuRd"
    else:
        cmap = "Spectral_r"
    plot_transform = cplt.rotated_pole_transform(data_ie)

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
    data_ie[v].plot(
        ax=ax,
        cmap=cmap,
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
# using Cork Airport met station coordinates
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

# %%
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
for v in data.data_vars:
    plt.figure(figsize=(12, 4))
    plt.plot(data_ie["time"], data_ie[v])
    plt.xlabel(data_ie["time"].attrs["standard_name"])
    plt.ylabel(
        data_ie[v].attrs["long_name"] + " [" + data_ie[v].attrs["units"] + "]"
    )
    plt.title(cplt.cordex_plot_title(data_ie, lon=LON, lat=LAT))
    plt.tight_layout()
    plt.show()

# %% [markdown]
# ## Read a subset (historical)

# %%
cordex_eur11 = cordex_eur11_cat.search(
    experiment_id="historical",
    variable_id=["pr", "tas", "evspsblpot"],
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

# %%
data.rio.crs

# %% [markdown]
# ### Ireland subset

# %%
# clip to Ireland's boundary with a 10 km buffer
data = data.rio.clip(ie.buffer(10000).to_crs(data.rio.crs))

# %%
data

# %% [markdown]
# ### Convert units

# %%
for v in data.data_vars:
    var_attrs = data[v].attrs  # extract attributes
    if v == "tas":
        var_attrs["units"] = "°C"  # convert K to deg C
        data[v] = data[v] - 273.15
    else:
        var_attrs["units"] = "mm/day"  # convert kg m-2 s-1 to mm/day
        data[v] = data[v] * 60 * 60 * 24
    data[v].attrs = var_attrs  # reassign attributes

# %%
data

# %% [markdown]
# ### Export data

# %%
# export to NetCDF
FILE_NAME = cplt.ie_cordex_ncfile_name(data)

# %%
data.to_netcdf(os.path.join(DATA_DIR, FILE_NAME))

# %% [markdown]
# #### Time subset

# %%
data_ie = data.isel(time=50)

# %%
data_ie

# %%
for v in data.data_vars:
    cbar_label = (
        data_ie[v].attrs["long_name"] + " [" + data_ie[v].attrs["units"] + "]"
    )  # colorbar label
    if v == "pr":
        cmap = "GnBu"
    elif v == "evspsblpot":
        cmap = "PuRd"
    else:
        cmap = "Spectral_r"
    plot_transform = cplt.rotated_pole_transform(data_ie)

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
    data_ie[v].plot(
        ax=ax,
        cmap=cmap,
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
# using Cork Airport met station coordinates
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

# %%
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
for v in data.data_vars:
    plt.figure(figsize=(12, 4))
    plt.plot(data_ie["time"], data_ie[v])
    plt.xlabel(data_ie["time"].attrs["standard_name"])
    plt.ylabel(
        data_ie[v].attrs["long_name"] + " [" + data_ie[v].attrs["units"] + "]"
    )
    plt.title(cplt.cordex_plot_title(data_ie, lon=LON, lat=LAT))
    plt.tight_layout()
    plt.show()
