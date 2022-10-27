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
    driving_model_id="MPI-M-MPI-ESM-LR"
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
# copy time_bnds coordinates
data_time_bnds = data.coords["time_bnds"]

# %%
# copy CRS
data_crs = data.rio.crs

# %%
data_crs

# %% [markdown]
# ### Ireland subset

# %%
# clip to Ireland's boundary
data = data.rio.clip(ie.buffer(500).to_crs(data_crs))

# %%
# reassign time_bnds
data.coords["time_bnds"] = data_time_bnds

# %%
data

# %% [markdown]
# ### Calculate photosynthetically active radiation

# %%
# Papaioannou et al. (1993) - irradiance ratio
data = data.assign(par=(data["rsds"] + data["rsus"]) * 0.473)

# %%
# drop original radiation data
data = data.drop_vars(["rsds", "rsus"])

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
    elif v == "par":
        var_attrs["long_name"] = "Surface Photosynthetically Active Radiation"
        var_attrs["units"] = "MJ m⁻² day⁻¹"  # convert W m-2 to MJ m-2 day-1
        # Allen (1998) - FAO Irrigation and Drainage Paper No. 56 (p. 45)
        # (per second to per day; then convert to mega)
        data[v] = data[v] * (60 * 60 * 24 / 1e6)
    elif v == "mrso":
        var_attrs["units"] = "mm day⁻¹"  # kg m-2 is the same as mm day-1
    elif v in ("pr", "evspsblpot"):
        var_attrs["units"] = "mm day⁻¹"  # convert kg m-2 s-1 to mm day-1
        data[v] = data[v] * 60 * 60 * 24  # (per second to per day)
    data[v].attrs = var_attrs  # reassign attributes

# %%
# assign attributes for the data
data.attrs["comment"] = (
    "This dataset has been clipped with the Island of Ireland's boundary. "
    "Last updated: " + str(datetime.now(tz=timezone.utc)) +
    " by nstreethran@ucc.ie."
)

# %%
data

# %% [markdown]
# ### Export data

# %%
# reassign CRS
data.rio.write_crs(data_crs, inplace=True)

# %%
data.rio.crs

# %%
# export to NetCDF
FILE_NAME = cplt.ie_cordex_ncfile_name(data)
data.to_netcdf(os.path.join(DATA_DIR, FILE_NAME))

# %% [markdown]
# ### Time subset

# %%
data_ie = data.sel(
    time=[
        str(year) + "-06-21T12:00:00.000000000" for year in sorted(
            list(set(data["time"].dt.year.values))
        )
    ]
)

# %%
data_ie

# %%
cplt.plot_facet_map_variables(data_ie, ie)

# %%
data_ie = data.sel(time="2055-06-21T12:00:00.000000000")

# %%
data_ie

# %%
cplt.plot_map_variables(data_ie)

# %% [markdown]
# ### Point subset

# %%
# using Cork Airport met station coordinates
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

# %%
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
data_ie

# %%
for v in data_ie.data_vars:
    plt.figure(figsize=(12, 4))
    plt.plot(data_ie["time"], data_ie[v], linewidth=.5)
    # plt.xlabel(data_ie["time"].attrs["standard_name"].capitalize())
    # plt.title(cplt.cordex_plot_title(data_ie, lon=LON, lat=LAT))
    plt.ylabel(
        f"{data_ie[v].attrs['long_name']}\n[{data_ie[v].attrs['units']}]"
    )
    plt.tight_layout()
    plt.show()

# %% [markdown]
# ## Read a subset (rcp45)

# %%
cordex_eur11 = cordex_eur11_cat.search(
    experiment_id="rcp45",
    driving_model_id="MPI-M-MPI-ESM-LR",
    variable_id=["evspsblpot", "mrso", "pr", "rsds", "tas"]
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
# copy time_bnds coordinates
data_time_bnds = data.coords["time_bnds"]

# %%
# copy CRS
data_crs = data.rio.crs

# %%
data_crs

# %% [markdown]
# ### Ireland subset

# %%
# clip to Ireland's boundary
data = data.rio.clip(ie.buffer(500).to_crs(data_crs))

# %%
# reassign time_bnds
data.coords["time_bnds"] = data_time_bnds

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
    elif v == "rsds":
        var_attrs["units"] = "MJ m⁻² day⁻¹"  # convert W m-2 to MJ m-2 day-1
        # Allen (1998) - FAO Irrigation and Drainage Paper No. 56 (p. 45)
        # (per second to per day; then convert to mega)
        data[v] = data[v] * (60 * 60 * 24 / 1e6)
    elif v == "mrso":
        var_attrs["units"] = "mm day⁻¹"  # kg m-2 is the same as mm day-1
    elif v in ("pr", "evspsblpot"):
        var_attrs["units"] = "mm day⁻¹"  # convert kg m-2 s-1 to mm day-1
        data[v] = data[v] * 60 * 60 * 24  # (per second to per day)
    data[v].attrs = var_attrs  # reassign attributes

# %%
# assign attributes for the data
data.attrs["comment"] = (
    "This dataset has been clipped with the Island of Ireland's boundary. "
    "Last updated: " + str(datetime.now(tz=timezone.utc)) +
    " by nstreethran@ucc.ie."
)

# %%
data

# %% [markdown]
# ### Export data

# %%
# reassign CRS
data.rio.write_crs(data_crs, inplace=True)

# %%
data.rio.crs

# %%
# export to NetCDF
FILE_NAME = cplt.ie_cordex_ncfile_name(data)
data.to_netcdf(os.path.join(DATA_DIR, FILE_NAME))

# %% [markdown]
# ### Time subset

# %%
data_ie = data.sel(
    time=[
        str(year) + "-06-21T12:00:00.000000000" for year in sorted(
            list(set(data["time"].dt.year.values))
        )
    ]
)

# %%
data_ie

# %%
cplt.plot_facet_map_variables(data_ie, ie)

# %%
data_ie = data.sel(time="2055-06-21T12:00:00.000000000")

# %%
data_ie

# %%
cplt.plot_map_variables(data_ie)

# %% [markdown]
# ### Point subset

# %%
# using Cork Airport met station coordinates
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

# %%
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
data_ie

# %%
for v in data_ie.data_vars:
    plt.figure(figsize=(12, 4))
    plt.plot(data_ie["time"], data_ie[v], linewidth=.5)
    # plt.xlabel(data_ie["time"].attrs["standard_name"].capitalize())
    # plt.title(cplt.cordex_plot_title(data_ie, lon=LON, lat=LAT))
    plt.ylabel(
        f"{data_ie[v].attrs['long_name']}\n[{data_ie[v].attrs['units']}]"
    )
    plt.tight_layout()
    plt.show()

# %% [markdown]
# ## Read a subset (historical)

# %%
cordex_eur11 = cordex_eur11_cat.search(
    experiment_id="historical",
    driving_model_id="MPI-M-MPI-ESM-LR",
    variable_id=["evspsblpot", "mrso", "pr", "rsds", "tas"]
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
# copy time_bnds coordinates
data_time_bnds = data.coords["time_bnds"]

# %%
# copy CRS
data_crs = data.rio.crs

# %%
data_crs

# %% [markdown]
# ### Ireland subset

# %%
# clip to Ireland's boundary
data = data.rio.clip(ie.buffer(500).to_crs(data_crs))

# %%
# reassign time_bnds
data.coords["time_bnds"] = data_time_bnds

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
    elif v == "rsds":
        var_attrs["units"] = "MJ m⁻² day⁻¹"  # convert W m-2 to MJ m-2 day-1
        # Allen (1998) - FAO Irrigation and Drainage Paper No. 56 (p. 45)
        # (per second to per day; then convert to mega)
        data[v] = data[v] * (60 * 60 * 24 / 1e6)
    elif v == "mrso":
        var_attrs["units"] = "mm day⁻¹"  # kg m-2 is the same as mm day-1
    elif v in ("pr", "evspsblpot"):
        var_attrs["units"] = "mm day⁻¹"  # convert kg m-2 s-1 to mm day-1
        data[v] = data[v] * 60 * 60 * 24  # (per second to per day)
    data[v].attrs = var_attrs  # reassign attributes

# %%
# assign attributes for the data
data.attrs["comment"] = (
    "This dataset has been clipped with the Island of Ireland's boundary. "
    "Last updated: " + str(datetime.now(tz=timezone.utc)) +
    " by nstreethran@ucc.ie."
)

# %%
data

# %% [markdown]
# ### Export data

# %%
# reassign CRS
data.rio.write_crs(data_crs, inplace=True)

# %%
data.rio.crs

# %%
# export to NetCDF
FILE_NAME = cplt.ie_cordex_ncfile_name(data)
data.to_netcdf(os.path.join(DATA_DIR, FILE_NAME))

# %% [markdown]
# ### Time subset

# %%
data_ie = data.sel(
    time=[
        str(year) + "-06-21T12:00:00.000000000" for year in sorted(
            list(set(data["time"].dt.year.values))
        )
    ]
)

# %%
data_ie

# %%
cplt.plot_facet_map_variables(data_ie, ie)

# %%
data_ie = data.sel(time="1990-06-21T12:00:00.000000000")

# %%
data_ie

# %%
cplt.plot_map_variables(data_ie)

# %% [markdown]
# ### Point subset

# %%
# using Cork Airport met station coordinates
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

# %%
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
data_ie

# %%
for v in data_ie.data_vars:
    plt.figure(figsize=(12, 4))
    plt.plot(data_ie["time"], data_ie[v], linewidth=.5)
    # plt.xlabel(data_ie["time"].attrs["standard_name"].capitalize())
    # plt.title(cplt.cordex_plot_title(data_ie, lon=LON, lat=LAT))
    plt.ylabel(
        f"{data_ie[v].attrs['long_name']}\n[{data_ie[v].attrs['units']}]"
    )
    plt.tight_layout()
    plt.show()
