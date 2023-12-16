#!/usr/bin/env python
# coding: utf-8

import glob
import os

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import xarray as xr
from rasterstats import zonal_stats
from shapely.geometry import Point

import climag.plot_configs as cplt

# ## Growth data

out = xr.open_mfdataset(
    os.path.join(
        "data", "ModVege", "MERA", "modvege_IE_MERA_FC3hr_3_day_*.nc"
    ),
    decode_coords="all",
    chunks="auto",
)

# limit to 2012-2019
out = out.sel(time=slice("2012-01-01", "2019-08-31"))

# keep only growth
out = out.drop_vars([i for i in out.data_vars if i != "gro"])

# ## Input data

ds = xr.open_dataset(
    os.path.join(
        "/run/media/nms/MyPassport", "MERA", "IE_MERA_FC3hr_3_day.nc"
    ),
    chunks="auto",
    decode_coords="all",
)

# ## Pasture mask

# Corine land cover 2018
# pasture only - vectorised (done in QGIS)
pasture = gpd.read_file(
    os.path.join("data", "landcover", "clc-2018", "clc-2018-pasture.gpkg"),
    layer="dissolved",
)

# reproject
pasture = pasture.to_crs(cplt.projection_lambert_conformal)

# mask out non-pasture areas
ds_ = ds.rio.clip(pasture["geometry"], all_touched=True)
out_ = out.rio.clip(pasture["geometry"], all_touched=True)

# ## Enniscorthy time series

# met station coords
# Wexford,4015,ENNISCORTHY (Brownswood),18,297870,135550,1983,(null)
point = gpd.GeoSeries(Point(-6.56083, 52.46306), crs=4326).to_crs(
    cplt.projection_lambert_conformal
)

# extract time series for Enniscorthy
ds_ = ds_.sel(x=float(point.x), y=float(point.y), method="nearest")
out_ = out_.sel(x=float(point.x), y=float(point.y), method="nearest")

# convert to dataframe
ds_ = ds_.to_dataframe()
out_ = out_.to_dataframe()

# columns to drop
columns_drop = ["x", "y", "height", "Lambert_Conformal", "spatial_ref"]

ts = pd.merge(
    ds_.drop(columns=columns_drop),
    out_.drop(columns=columns_drop),
    left_index=True,
    right_index=True,
)


def get_linear_regression(plot_data, xds, x, y, season=None):
    if season == "MAM":
        plot_data = plot_data[
            (plot_data.index.month == 3)
            | (plot_data.index.month == 4)
            | (plot_data.index.month == 5)
        ]
    elif season == "JJA":
        plot_data = plot_data[
            (plot_data.index.month == 6)
            | (plot_data.index.month == 7)
            | (plot_data.index.month == 8)
        ]
    elif season == "SON":
        plot_data = plot_data[
            (plot_data.index.month == 9)
            | (plot_data.index.month == 10)
            | (plot_data.index.month == 11)
        ]
    elif season == "DJF":
        plot_data = plot_data[
            (plot_data.index.month == 12)
            | (plot_data.index.month == 1)
            | (plot_data.index.month == 2)
        ]

    model = sm.OLS(plot_data[y], sm.add_constant(plot_data[x]))
    results = model.fit()

    print(results.summary())

    fig = sns.jointplot(
        x=x,
        y=y,
        data=plot_data,
        color="lightskyblue",
        marginal_kws=dict(bins=25),
    )
    b, m = results.params
    r = results.rsquared
    plt.axline(
        (0, b),
        slope=m,
        label=f"$y = {m:.2f}x {b:+.2f}$\n$R^2 = {r:.2f}$",
        color="crimson",
        linewidth=2,
    )
    plt.legend(loc="upper left")
    plt.xlabel(f"{xds[x].attrs['long_name']} [{xds[x].attrs['units']}]")
    plt.ylabel("Simulated grass growth [kg DM ha⁻¹ day⁻¹]")
    plt.tight_layout()
    plt.show()


# ### Winter

for var in ds.data_vars:
    print("Variable:", var)
    get_linear_regression(ts, ds, var, "gro", "DJF")

# ### Autumn

for var in ds.data_vars:
    print("Variable:", var)
    get_linear_regression(ts, ds, var, "gro", "SON")

# ### Summer

for var in ds.data_vars:
    print("Variable:", var)
    get_linear_regression(ts, ds, var, "gro", "JJA")

# ### Spring

for var in ds.data_vars:
    print("Variable:", var)
    get_linear_regression(ts.dropna(), ds, var, "gro", "MAM")

# ### All seasons

for var in ds.data_vars:
    print("Variable:", var)
    get_linear_regression(ts.dropna(), ds, var, "gro", None)
