#!/usr/bin/env python
# coding: utf-8

# # ModVege results - EURO-CORDEX - Difference in mean - historical and observational (MÉRA)
#
# - Weighted means take into account the number of days in each month

# import libraries
import glob
import os
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
import rasterio as rio
import xarray as xr
import climag.plot_configs as cplt
import climag.plot_stats as cstats
import importlib

season_list = ["DJF", "MAM", "JJA", "SON"]

data = cstats.hist_obs_diff(stat="mean", dataset="EURO-CORDEX")

importlib.reload(cstats)

# ## Total growth (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="gro",
        season=season,
        levels=cstats.colorbar_levels(60, num=5),
        ticks=[-60 + 20 * n for n in range(7)],
    )

# ## Potential growth (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="pgro",
        season=season,
        levels=cstats.colorbar_levels(75, num=5),
        ticks=[-75 + 25 * n for n in range(7)],
    )

# ## Total ingestion (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="c_bm",
        season=season,
        levels=cstats.colorbar_levels(12.5, num=1.25),
        ticks=[-12.5 + 2.5 * n for n in range(11)],
    )

# ## Standing biomass (cumulative)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="bm",
        season=season,
        levels=cstats.colorbar_levels(2500, num=250),
        ticks=[-2500 + 500 * n for n in range(11)],
    )

# ## Defoliation (senescence + abscission) (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="sen_abs",
        season=season,
        levels=cstats.colorbar_levels(80, num=10),
        ticks=[-80 + 20 * n for n in range(9)],
    )

# ## Total biomass consumption (ingested + harvested) (yearly total)

importlib.reload(cstats)

cstats.plot_obs_diff_all(
    data=data["MERA_c_diff"],
    var="c_bm_all",
    season=None,
    levels=cstats.colorbar_levels(3000, num=250),
    ticks=[-3000 + 1000 * n for n in range(7)],
)

print("Last updated:", datetime.now(tz=timezone.utc))
