#!/usr/bin/env python
# coding: utf-8

# # Seasonal stats - HiResIreland - Difference in maximum - historical and observational (MÉRA)

import importlib
# import libraries
from datetime import datetime, timezone

import climag.plot_stats as cstats

season_list = ["DJF", "MAM", "JJA", "SON"]

data = cstats.hist_obs_diff(stat="max", dataset="HiResIreland")

importlib.reload(cstats)

# ## Total growth (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="gro",
        season=season,
        levels=cstats.colorbar_levels(100),
        ticks=cstats.colorbar_ticks(100),
    )

# ## Potential growth (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="pgro",
        season=season,
        levels=cstats.colorbar_levels(150),
        ticks=cstats.colorbar_ticks(150),
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
        levels=cstats.colorbar_levels(3000),
        ticks=cstats.colorbar_ticks(3000),
    )

# ## Defoliation (senescence + abscission) (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="sen_abs",
        season=season,
        levels=cstats.colorbar_levels(150),
        ticks=cstats.colorbar_ticks(150),
    )

# ## Total biomass consumption (ingested + harvested) (yearly total)

cstats.plot_obs_diff_all(
    data=data["MERA_c_diff"],
    var="c_bm_all",
    season=None,
    levels=cstats.colorbar_levels(4000),
    ticks=cstats.colorbar_ticks(4000),
)

print("Last updated:", datetime.now(tz=timezone.utc))
