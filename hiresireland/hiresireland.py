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
import xarray as xr
import climag.plot_configs as cplt

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR_BASE = os.path.join("data", "HiResIreland")

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
GPKG_BOUNDARY = os.path.join(
    "data", "boundaries", "NUTS2021", "NUTS_2021.gpkg"
)
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")

# %% [markdown]
# ## rcp45

# %%
data = xr.open_mfdataset(
    list(itertools.chain(*list(
        glob.glob(os.path.join(
            DATA_DIR_BASE, "COSMO5-CLM", "rcp45", "MPI-ESM-LR", e
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
data = data.rio.clip(ie.buffer(1).to_crs(data_crs))

# %%
# reassign time_bnds
data.coords["time_bnds"] = data_time_bnds

# %%
data

# %% [markdown]
# ### Calculate photosynthetically active radiation

# %%
# Papaioannou et al. (1993) - irradiance ratio
data = data.assign(par=(data["ASOB_S"] * 0.473))

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
    elif v in ("ASOB_S", "par"):
        var_attrs["units"] = "MJ m⁻² day⁻¹"  # convert W m-2 to MJ m-2 day-1
        # Allen (1998) - FAO Irrigation and Drainage Paper No. 56 (p. 45)
        # (per second to per day; then convert to mega)
        data[v] = data[v] * (60 * 60 * 24 / 1e6)
        if v == "par":
            var_attrs["long_name"] = (
                "Surface Photosynthetically Active Radiation"
            )
            var_attrs["note"] = (
                "Calculated by multiplying 'rsds' with an irradiance ratio of"
                " 0.473 based on Papaioannou et al. (1993); converted from "
                "W m⁻² to MJ m⁻² day⁻¹ by multiplying 0.0864 based on the FAO"
                " Irrigation and Drainage Paper No. 56 (Allen et al., 1998, "
                "p. 45)"
            )
        else:
            var_attrs["long_name"] = "Surface Downwelling Shortwave Radiation"
            var_attrs["note"] = (
                f"Original name is '{v}'; converted from W m⁻² to "
                "MJ m⁻² day⁻¹ by multiplying 0.0864 based on the FAO "
                "Irrigation and Drainage Paper No. 56 "
                "(Allen et al., 1998, p. 45)"
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
    "T_2M": "T", "ASOB_S": "RG", "TOT_PREC": "PP", "w": "PET", "par": "PAR"
})

# %%
# assign attributes for the data
data.attrs["comment"] = (
    "This dataset has been clipped with the Island of Ireland's boundary and "
    "units have been converted. "
    "Last updated: " + str(datetime.now(tz=timezone.utc)) +
    " by nstreethran@ucc.ie."
)

# %%
# remove dataset history
del data.attrs["history"]

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
FILE_NAME = "IE_" + data.attrs["title"] + ".nc"
data.to_netcdf(os.path.join(DATA_DIR, FILE_NAME))

# %% [markdown]
# ### Time subset

# %%
data_ie = data.sel(
    time=[
        str(year) + "-06-15T10:30:00.000000000" for year in sorted(
            list(set(data["time"].dt.year.values))
        )
    ]
)

# %%
data_ie

# %%
cplt.plot_facet_map_variables(data_ie, ie)

# %% [markdown]
# ### Point subset

# %%
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
