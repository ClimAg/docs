#!/usr/bin/env python
# coding: utf-8

# # Compare climate model dataset simulated values with measured averages - HiResIreland

import importlib
import os
from datetime import datetime, timezone
from itertools import product

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
from rasterstats import zonal_stats

import climag.plot_configs as cplt
import climag.plot_stats as cstats

ie_bbox = gpd.read_file(
    os.path.join("data", "boundaries", "boundaries_all.gpkg"),
    layer="ne_10m_land_2157_IE_BBOX_DIFF",
)

data = cstats.hist_rcp_stats_data(
    dataset="HiResIreland", stat="mean", diff=False
)["HiResIreland_s"].drop_vars(["bm", "sen_abs", "c_bm", "pgro"])

data

data_crs = data.rio.crs

counties = gpd.read_file(
    os.path.join("data", "boundaries", "boundaries_all.gpkg"),
    layer="OSi_OSNI_IE_Counties_2157",
)
counties["COUNTY"] = counties["COUNTY"].str.title()
counties.set_index("COUNTY", inplace=True)

counties

ts = pd.read_csv(os.path.join("data", "grass_growth", "average_growth.csv"))
ts.set_index("county", inplace=True)

ts

ts_2018 = pd.read_csv(
    os.path.join("data", "grass_growth", "average_growth_2018.csv")
)
ts_2018.set_index("county", inplace=True)

ts_2018

data_county = {}
for county in ts.index:
    data_county[county] = data.rio.clip(
        counties.loc[[county]].to_crs(data_crs)["geometry"], all_touched=True
    )

data_county_mam = data_county.copy()

for key in data_county_mam.keys():
    data_county_mam[key] = data_county_mam[key].sel(season="MAM")
    data_county_mam[key] = data_county_mam[key].assign(
        gro_diff=data_county_mam[key]["gro"] - ts.loc[county]["MAM"]
    )
    data_county_mam[key] = data_county_mam[key].assign(
        gro_diff_2018=(
            data_county_mam[key]["gro"] - ts_2018.loc[county]["2018 (MAM)"]
        )
    )

data_county_mam = xr.merge(data_county_mam.values())

data_county_jja = data_county.copy()

for key in data_county_jja.keys():
    data_county_jja[key] = data_county_jja[key].sel(season="JJA")
    data_county_jja[key] = data_county_jja[key].assign(
        gro_diff=data_county_jja[key]["gro"] - ts.loc[county]["JJA"]
    )
    data_county_jja[key] = data_county_jja[key].assign(
        gro_diff_2018=(
            data_county_jja[key]["gro"] - ts_2018.loc[county]["2018 (JJA)"]
        )
    )

data_county_jja = xr.merge(data_county_jja.values())


def data_plot(data, var, levels=None, ticks=None):
    fig = data[var].plot.contourf(
        x="rlon",
        y="rlat",
        transform=cplt.rotated_pole_transform(data),
        subplot_kws={"projection": cplt.projection_hiresireland},
        cmap="BrBG",
        col="model",
        row="exp",
        xlim=(-1.9, 1.6),
        ylim=(-2.1, 2.1),
        extend="both",
        figsize=(12, 13.75),
        levels=levels,
        cbar_kwargs={
            "ticks": ticks,
            "aspect": 30,
            "location": "bottom",
            "fraction": 0.085,
            "shrink": 0.85,
            "pad": 0.05,
            "extendfrac": "auto",
            "label": "Difference [kg DM ha⁻¹ day⁻¹]",
        },
    )
    for (col, model), (row, exp) in product(
        enumerate(data["model"].values), enumerate(data["exp"].values)
    ):
        ie_bbox.to_crs(cplt.projection_hiresireland).plot(
            ax=fig.axs[row][col],
            edgecolor="darkslategrey",
            color="white",
            linewidth=0.5,
        )
    fig.set_titles("{value}", weight="semibold", fontsize=14)
    plt.show()


# ## Compare growth with seasonal averages

data_plot(
    data_county_mam,
    "gro_diff",
    cstats.colorbar_levels(60),
    cstats.colorbar_ticks(60),
)

data_plot(
    data_county_jja,
    "gro_diff",
    cstats.colorbar_levels(120),
    cstats.colorbar_ticks(120),
)

# ## Compare growth with 2018 seasonal averages

data_plot(
    data_county_mam,
    "gro_diff_2018",
    cstats.colorbar_levels(60),
    cstats.colorbar_ticks(60),
)

data_plot(
    data_county_jja,
    "gro_diff_2018",
    cstats.colorbar_levels(120),
    cstats.colorbar_ticks(120),
)
