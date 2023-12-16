#!/usr/bin/env python
# coding: utf-8

# # ModVege results - EURO-CORDEX - Difference in unbiased standard deviation - historical and observational (MÉRA)

import importlib
# import libraries
from datetime import datetime, timezone

import climag.plot_stats as cstats

season_list = ["DJF", "MAM", "JJA", "SON"]

data = cstats.hist_obs_diff(stat="std", dataset="HiResIreland")

importlib.reload(cstats)

# ## Total growth (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="gro",
        season=season,
        levels=cstats.colorbar_levels(30),
        ticks=cstats.colorbar_ticks(30),
    )

# ## Potential growth (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="pgro",
        season=season,
        levels=cstats.colorbar_levels(50),
        ticks=cstats.colorbar_ticks(50),
    )

# ## Total ingestion (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="c_bm",
        season=season,
        levels=cstats.colorbar_levels(7.5),
        ticks=cstats.colorbar_ticks(7.5),
    )

# ## Standing biomass (cumulative)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="bm",
        season=season,
        levels=cstats.colorbar_levels(750),
        ticks=cstats.colorbar_ticks(750),
    )

# ## Defoliation (senescence + abscission) (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="sen_abs",
        season=season,
        levels=cstats.colorbar_levels(30),
        ticks=cstats.colorbar_ticks(30),
    )

# ## Total biomass consumption (ingested + harvested) (yearly total)

cstats.plot_obs_diff_all(
    data=data["MERA_c_diff"],
    var="c_bm_all",
    season=None,
    levels=cstats.colorbar_levels(600),
    ticks=cstats.colorbar_ticks(600),
)

print("Last updated:", datetime.now(tz=timezone.utc))
