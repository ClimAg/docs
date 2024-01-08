#!/usr/bin/env python
# coding: utf-8

# # Create MERA time series for comparison with measurements

import os
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
from rasterstats import zonal_stats
import climag.climag as cplt

# ## Model results

ds = xr.open_mfdataset(
    os.path.join(
        "data", "ModVege", "MERA", "modvege_IE_MERA_FC3hr_3_day_*.nc"
    ),
    decode_coords="all",
    chunks="auto",
)

# limit to MERA time series
ds = ds.sel(time=slice("1981-01-01", "2019-08-31"))

# keep only growth
ds = ds.drop_vars([i for i in ds.data_vars if i != "gro"])

# # resample - yearly average
# ds_ = cplt.weighted_average(data=ds, averages="year")

# resample - weekly average
ds_ = ds.resample(time="W-MON").mean()

for var in ds_.data_vars:
    ds_[var].attrs = ds[var].attrs

ds_.rio.write_crs(cplt.projection_lambert_conformal, inplace=True)

# ## County boundaries

counties = gpd.read_file(
    os.path.join("data", "boundaries", "boundaries_all.gpkg"),
    layer="OSi_OSNI_IE_Counties_2157",
)

# ## Land cover

# Corine land cover 2018
# pasture only - vectorised (done in QGIS)
pasture = gpd.read_file(
    os.path.join("data", "landcover", "clc-2018", "clc-2018-pasture.gpkg"),
    layer="dissolved",
)

# ## Zonal stats

os.makedirs(os.path.join("data", "ModVege", "growth", "week"), exist_ok=True)

# save each week as netCDF
for t in ds_["time"].values:
    ds_.sel(time=str(t)[:10]).to_netcdf(
        os.path.join(
            "data",
            "ModVege",
            "growth",
            "week",
            f"MERA_growth_{str(t)[:10]}.nc",
        )
    )

stats = {}

for t in ds_["time"].values:
    stats[str(t)[:10]] = gpd.GeoDataFrame.from_features(
        zonal_stats(
            vectors=counties.to_crs(cplt.projection_lambert_conformal),
            raster=os.path.join(
                "data",
                "ModVege",
                "growth",
                "week",
                f"MERA_growth_{str(t)[:10]}.nc",
            ),
            stats=["mean"],
            geojson_out=True,
            all_touched=True,
        )
    )
    stats[str(t)[:10]].drop(
        columns=["geometry", "PROVINCE", "CONTAE"], inplace=True
    )
    stats[str(t)[:10]]["time"] = str(t)[:10]

all_data = pd.concat([df for df in stats.values()], ignore_index=True)

all_data.head()

all_data.to_csv(
    os.path.join("data", "ModVege", "growth", "MERA_growth_week_all.csv"),
    index=False,
)

# ## Zonal stats - only for pastures

os.makedirs(
    os.path.join("data", "ModVege", "growth", "week_pasture"), exist_ok=True
)

# mask out non-pasture areas
ds_ = ds_.rio.clip(
    pasture["geometry"].to_crs(cplt.projection_lambert_conformal),
    all_touched=True,
)

plt.figure(figsize=(7, 7))
axs = plt.axes(projection=cplt.projection_lambert_conformal)
ds_.isel(time=30)["gro"].plot.contourf(cmap="YlGn", ax=axs)
pasture.to_crs(cplt.projection_lambert_conformal).boundary.plot(
    linewidth=0.1, ax=axs, color="black"
)
plt.tight_layout()
plt.show()

# save each week as netCDF
for t in ds_["time"].values:
    ds_.sel(time=str(t)[:10]).to_netcdf(
        os.path.join(
            "data",
            "ModVege",
            "growth",
            "week_pasture",
            f"MERA_growth_{str(t)[:10]}.nc",
        )
    )

stats = {}

for t in ds_["time"].values:
    stats[str(t)[:10]] = gpd.GeoDataFrame.from_features(
        zonal_stats(
            vectors=counties.to_crs(cplt.projection_lambert_conformal),
            raster=os.path.join(
                "data",
                "ModVege",
                "growth",
                "week_pasture",
                f"MERA_growth_{str(t)[:10]}.nc",
            ),
            stats=["mean"],
            geojson_out=True,
            all_touched=True,
        )
    )
    stats[str(t)[:10]].drop(
        columns=["geometry", "PROVINCE", "CONTAE"], inplace=True
    )
    stats[str(t)[:10]]["time"] = str(t)[:10]

all_data = pd.concat([df for df in stats.values()], ignore_index=True)

all_data.head()

all_data.shape

all_data.to_csv(
    os.path.join("data", "ModVege", "growth", "MERA_growth_week_pasture.csv"),
    index=False,
)

