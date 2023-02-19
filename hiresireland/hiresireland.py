# %% [markdown]
# # HiResIreland

# %%
# import libraries
import glob
import itertools
import os
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
from dask.distributed import Client
import climag.plot_configs as cplt

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
client = Client(n_workers=3, threads_per_worker=4, memory_limit="2GB")

# %%
client

# %%
DATA_DIR_BASE = os.path.join("data", "HiResIreland")

# %%
# directory to store outputs
DATA_DIR = os.path.join(DATA_DIR_BASE, "IE")
os.makedirs(DATA_DIR, exist_ok=True)

# %%
# Valentia Observatory met station coords
LON, LAT = -10.24333, 51.93806

# %%
# using Valentia Observatory met station coordinates
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

# %%
# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")
ie_bbox = gpd.read_file(
    GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE_BBOX_DIFF"
)

# %% [markdown]
# ## rcp45

# %%
data = xr.open_mfdataset(
    list(itertools.chain(*list(
        glob.glob(os.path.join(
            DATA_DIR_BASE, "COSMO5-CLM", "rcp45", "EC-EARTH", e
        ))
        for e in ["*mean_T_2M*.nc", "*ASOB_S*.nc", "*ET*.nc", "*TOT_PREC*.nc"]
    ))),
    chunks="auto",
    decode_coords="all"
)

# %%
data

# %%
# copy time_bnds
# data_time_bnds = data.coords["time_bnds"]

# %%
# copy CRS
data_crs = data.rio.crs

# %%
data_crs

# %% [markdown]
# ### Ireland subset

# %%
# clip to Ireland's boundary
data = data.rio.clip(ie.buffer(1).to_crs(data_crs))

# %%
# reassign time_bnds
# data.coords["time_bnds"] = data_time_bnds

# %%
data

# %% [markdown]
# ### Calculate downward shortwave radiation

# %%
# assume an albedo of 0.23 for grass (Allen et al., 1998)
data = data.assign(RS=data["ASOB_S"] / (1 - 0.23))

# %%
data

# %% [markdown]
# ### Calculate photosynthetically active radiation

# %%
# Papaioannou et al. (1993) - irradiance ratio
data = data.assign(PAR=data["RS"] * 0.473)

# %%
data

# %% [markdown]
# ### Convert units and rename variables

# %%
for v in data.data_vars:
    var_attrs = data[v].attrs  # extract attributes
    if v == "T_2M":
        var_attrs["units"] = "°C"  # convert K to deg C
        data[v] = data[v] - 273.15
        var_attrs["note"] = (
            f"Original name is '{v}'; converted from K to °C by subtracting "
            "273.15"
        )
        var_attrs["long_name"] = "Near-Surface Air Temperature"
    elif v in ("ASOB_S", "PAR", "RS"):
        var_attrs["units"] = "MJ m⁻² day⁻¹"  # convert W m-2 to MJ m-2 day-1
        # Allen (1998) - FAO Irrigation and Drainage Paper No. 56 (p. 45)
        # (per second to per day; then convert to mega)
        data[v] = data[v] * (60 * 60 * 24 / 1e6)
        if v == "PAR":
            var_attrs["long_name"] = (
                "Surface Photosynthetically Active Radiation"
            )
            var_attrs["note"] = (
                "Calculated by multiplying ASOB_S with an irradiance ratio of"
                " 0.473 based on Papaioannou et al. (1993); converted from "
                "W m⁻² to MJ m⁻² day⁻¹ by multiplying 0.0864 based on the FAO"
                " Irrigation and Drainage Paper No. 56 (Allen et al., 1998, "
                "p. 45)"
            )
        elif v == "RS":
            var_attrs["long_name"] = (
                "Surface Downwelling Shortwave Radiation"
            )
        else:
            var_attrs["long_name"] = (
                "Surface Net Downward Shortwave Radiation"
            )
    elif v in ("TOT_PREC", "w"):
        var_attrs["units"] = "mm day⁻¹"  # kg m-2 is the same as mm day-1
        var_attrs["note"] = (
            f"Original name is '{v}'; kg m⁻² is equivalent to mm day⁻¹, "
            "assuming a water density of 1,000 kg m⁻³"
        )
        if v == "w":
            var_attrs["long_name"] = "Potential Evapotranspiration"
        else:
            var_attrs["long_name"] = "Precipitation"
    data[v].attrs = var_attrs  # reassign attributes

# %%
# rename
data = data.rename({
    "T_2M": "T", "ASOB_S": "RSN", "TOT_PREC": "PP", "w": "PET"
})

# %%
# remove dataset history
del data.attrs["history"]

# %%
# assign dataset name
data.attrs["dataset"] = f"IE_HiResIreland_{data.attrs['title'][:-4]}"

# %%
# assign attributes for the data
data.attrs["comment"] = (
    "This dataset has been clipped with the Island of Ireland's boundary and "
    "units have been converted. "
    "Last updated: " + str(datetime.now(tz=timezone.utc)) +
    " by nstreethran@ucc.ie."
)

# %%
data

# %% [markdown]
# ### Monthly averages

# %%
cplt.plot_averages(
    data=data, var="T", averages="month", boundary_data=ie_bbox,
    cbar_levels=[3 + 1 * n for n in range(13)]
)

# %%
for var in data.data_vars:
    cplt.plot_averages(
        data=data, var=var, averages="month", boundary_data=ie_bbox,
        cbar_levels=16
    )

# %% [markdown]
# ### Seasonal averages

# %%
for var in data.data_vars:
    cplt.plot_averages(
        data=data, var=var, averages="season", boundary_data=ie_bbox,
        cbar_levels=14
    )

# %% [markdown]
# ### Point subset

# %%
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
data_ie

# %%
for var in data.data_vars:
    plt.figure(figsize=(12, 4))
    plt.plot(data_ie["time"], data_ie[var], linewidth=.5)
    plt.title(f"{data_ie.attrs['dataset']}, lon={LON}, lat={LAT}")
    plt.ylabel(
        f"{data_ie[var].attrs['long_name']}\n[{data_ie[var].attrs['units']}]"
    )
    plt.tight_layout()
    plt.show()

# %%
data_ie = data_ie.sel(time=slice("2054", "2056"))

# %%
for var in data.data_vars:
    plt.figure(figsize=(12, 4))
    plt.plot(data_ie["time"], data_ie[var], linewidth=1)
    plt.title(f"{data_ie.attrs['dataset']}, lon={LON}, lat={LAT}")
    plt.ylabel(
        f"{data_ie[var].attrs['long_name']}\n[{data_ie[var].attrs['units']}]"
    )
    plt.tight_layout()
    plt.show()

# %%
data_ie_df = pd.DataFrame({"time": data_ie["time"]})
for var in ["RS", "RSN", "PAR"]:
    data_ie_df[var] = data_ie[var]

data_ie_df.set_index("time", inplace=True)

data_ie_df.plot(figsize=(12, 4), colormap="viridis", xlabel="")

plt.tight_layout()
plt.show()

# %%
data_ie_df = pd.DataFrame({"time": data_ie["time"]})
# configure plot title
plot_title = []
for var in ["T", "PP", "PET", "PAR"]:
    data_ie_df[var] = data_ie[var]
    plot_title.append(
        f"{data_ie[var].attrs['long_name']} [{data_ie[var].attrs['units']}]"
    )

data_ie_df.set_index("time", inplace=True)

data_ie_df.plot(
    subplots=True, layout=(4, 1), figsize=(9, 11),
    legend=False, xlabel="", title=plot_title
)

plt.tight_layout()
plt.show()

# %% [markdown]
# ### Extend data to a spin-up year

# %%
data_interp = data.interp(
    time=pd.date_range(
        f"{int(data['time'][0].dt.year) - 1}-01-01T10:30:00",
        f"{int(data['time'][0].dt.year) - 1}-12-31T10:30:00",
        freq="D"
    ),
    kwargs={"fill_value": None}
)

# %%
data_interp.rio.write_crs(data_crs, inplace=True)

# %%
# merge spin-up year with first two years of the main data
data_interp = xr.combine_by_coords([
    data_interp,
    data.sel(
        time=slice(
            str(int(data["time"][0].dt.year)),
            str(int(data["time"][0].dt.year) + 1)
        )
    )
])

# %%
data_interp

# %%
data_ie = data_interp.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
plt.figure(figsize=(12, 4))
plt.plot(data_ie["time"], data_ie["T"], linewidth=1)
plt.title(f"{data_ie.attrs['dataset']}, lon={LON}, lat={LAT}")
plt.ylabel(
    f"{data_ie['T'].attrs['long_name']}\n[{data_ie['T'].attrs['units']}]"
)
plt.tight_layout()
plt.show()

# %%
# check value for the first day of the first year
data_ie["T"][data_interp.sel(
    time=str(int(data_interp["time"][0].dt.year))
).dims["time"]].values

# %%
# check first value of spin-up year - should be nan
data_ie["T"][0].values

# %%
# shift first year of the main data to the spin-up year
data_interp = data_interp.shift(
    time=-data_interp.sel(
        time=str(int(data_interp["time"][0].dt.year))
    ).dims["time"]
)

# %%
data_ie = data_interp.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
# should be the same as before, but shifted forwards to the spin-up year
plt.figure(figsize=(12, 4))
plt.plot(data_ie["time"], data_ie["T"], linewidth=1)
plt.title(f"{data_ie.attrs['dataset']}, lon={LON}, lat={LAT}")
plt.ylabel(
    f"{data_ie['T'].attrs['long_name']}\n[{data_ie['T'].attrs['units']}]"
)
plt.tight_layout()
plt.show()

# %%
# check first value
data_ie["T"][0].values

# %%
# keep only spin-up year
data_interp = data_interp.sel(time=str(int(data_interp["time"][0].dt.year)))

# %%
data_interp

# %%
# merge with main dataset
data = xr.combine_by_coords([data, data_interp])

# %%
data

# %%
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest").sel(
    time=slice("2040", "2042")
)

# %%
# spin-up year and first year should be identical
plt.figure(figsize=(12, 4))
plt.plot(data_ie["time"], data_ie["T"], linewidth=1)
plt.title(f"{data_ie.attrs['dataset']}, lon={LON}, lat={LAT}")
plt.ylabel(
    f"{data_ie['T'].attrs['long_name']}\n[{data_ie['T'].attrs['units']}]"
)
plt.tight_layout()
plt.show()

# %%
data.rio.crs

# %% [markdown]
# ### Save data

# %%
# keep only relevant variables
data = data.drop_vars(["RS", "RSN"])

# %%
data.to_netcdf(os.path.join(DATA_DIR, f"{data.attrs['dataset']}.nc"))

# %%
# test if the data can be read without issues
data = xr.open_dataset(
    os.path.join(DATA_DIR, f"{data.attrs['dataset']}.nc"),
    chunks="auto",
    decode_coords="all"
)

# %%
data

# %%
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest").sel(
    time=slice("2040", "2044")
)

# %%
# spin-up year and first year should be identical
plt.figure(figsize=(12, 4))
plt.plot(data_ie["time"], data_ie["T"], linewidth=1)
plt.title(f"{data_ie.attrs['dataset']}, lon={LON}, lat={LAT}")
plt.ylabel(
    f"{data_ie['T'].attrs['long_name']}\n[{data_ie['T'].attrs['units']}]"
)
plt.tight_layout()
plt.show()
