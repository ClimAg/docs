#!/usr/bin/env python
# coding: utf-8

# # ModVege results - HiResIreland - Difference in min - historical and observational (MÉRA)

import importlib
# import libraries
from datetime import datetime, timezone

import climag.plot_stats as cstats

season_list = ["DJF", "MAM", "JJA", "SON"]

data = cstats.hist_obs_diff(stat="min", dataset="HiResIreland")

importlib.reload(cstats)

# ## Total growth (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="gro",
        season=season,
        levels=cstats.colorbar_levels(15),
        ticks=cstats.colorbar_ticks(15),
    )

# ## Potential growth (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="pgro",
        season=season,
        levels=cstats.colorbar_levels(32),
        ticks=cstats.colorbar_ticks(32),
    )

# ## Total ingestion (daily)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="c_bm",
        season=season,
        levels=cstats.colorbar_levels(22.5),
        ticks=cstats.colorbar_ticks(22.5),
    )

# ## Standing biomass (cumulative)

for season in season_list:
    cstats.plot_obs_diff_all(
        data=data["MERA_s_diff"],
        var="bm",
        season=season,
        levels=cstats.colorbar_levels(1250),
        ticks=cstats.colorbar_ticks(1250),
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
    levels=cstats.colorbar_levels(3200),
    ticks=cstats.colorbar_ticks(3200),
)

print("Last updated:", datetime.now(tz=timezone.utc))
