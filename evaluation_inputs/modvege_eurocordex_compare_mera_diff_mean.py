#!/usr/bin/env python
# coding: utf-8

# # Seasonal stats - EURO-CORDEX - Difference in (weighted) mean - historical and observational (MÉRA)
#
# - Weighted means take into account the number of days in each month

import importlib
import os
from datetime import datetime, timezone

import climag.plot_stats as cstats

season_list = ["DJF", "MAM", "JJA", "SON"]

data = cstats.hist_obs_diff(stat="mean", dataset="EURO-CORDEX")

importlib.reload(cstats)

# ## Total growth (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="gro",
        season=season,
        levels=cstats.colorbar_levels(60),
        ticks=cstats.colorbar_ticks(60),
    )

# ## Potential growth (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="pgro",
        season=season,
        levels=cstats.colorbar_levels(75),
        ticks=cstats.colorbar_ticks(75),
    )

# ## Total ingestion (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="c_bm",
        season=season,
        levels=cstats.colorbar_levels(12.5),
        ticks=cstats.colorbar_ticks(12.5),
    )

# ## Standing biomass (cumulative)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="bm",
        season=season,
        levels=cstats.colorbar_levels(2500),
        ticks=cstats.colorbar_ticks(2500),
    )

# ## Defoliation (senescence + abscission) (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="sen_abs",
        season=season,
        levels=cstats.colorbar_levels(80),
        ticks=cstats.colorbar_ticks(80),
    )

# ## Total biomass consumption (ingested + harvested) (yearly total)

cstats.plot_obs_diff_all(
    data=data["MERA_c_diff"],
    var="c_bm_all",
    season=None,
    levels=cstats.colorbar_levels(3000),
    ticks=cstats.colorbar_ticks(3000),
)
