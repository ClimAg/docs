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
import itertools
import pandas as pd
from sqlalchemy import create_engine

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
# filter data subset
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
data.dims

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

# %%
# len(list(itertools.product(
#     range(len(data["pr"]["rlon"])), range(len(data["pr"]["rlat"]))
# ))) == len(data["pr"]["rlon"]) * len(data["pr"]["rlat"])

# %%
# TS_OUT_DIR = os.path.join(
#     os.path.split(cordex_eur11.df["uri"][0])[0], "timeseries"
# )
# TS_FILE_BASE = os.path.split(cordex_eur11.df["uri"][0])[1][:-20]
# engine = create_engine("sqlite://", echo=False)
# os.makedirs(TS_OUT_DIR, exist_ok=True)
# for x, y in itertools.product(
#     range(len(data["pr"]["rlon"])), range(len(data["pr"]["rlat"]))
# ):
#     data_ie = data.isel(rlon=x, rlat=y)
#     data_df = pd.DataFrame(
#         {"time": data_ie["pr"]["time"], "pr": data_ie["pr"]}
#     )
#     if data_df["pr"].isna().all() == False:
#         TS_OUT_FILE = os.path.join(
#             TS_OUT_DIR, TS_FILE_BASE + str(x) + "-" + str(y) + ".csv"
#         )
#         data_df.to_csv(TS_OUT_FILE, index=False)

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
    if v == "tas":
        cmap = "Spectral_r"
    else:
        cmap = "GnBu"
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
