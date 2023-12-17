#!/usr/bin/env python
# coding: utf-8

# # Seasonal stats - EURO-CORDEX - Difference in (unbiased) standard deviation - historical and rcp45/rcp85

import importlib
from datetime import datetime, timezone

import climag.plot_stats as cstats

season_list = ["DJF", "MAM", "JJA", "SON"]

data = cstats.hist_rcp_stats_data(dataset="EURO-CORDEX", stat="std")

importlib.reload(cstats)

# ## Total growth (daily)

for season in season_list:
    cstats.plot_all(
        data=data["EURO-CORDEX_s"],
        var="gro",
        season=season,
        levels=cstats.colorbar_levels(12),
        ticks=cstats.colorbar_ticks(12),
    )

# ## Potential growth (daily)

for season in season_list:
    cstats.plot_all(
        data=data["EURO-CORDEX_s"],
        var="pgro",
        season=season,
        levels=cstats.colorbar_levels(24),
        ticks=cstats.colorbar_ticks(24),
    )

# ## Total ingestion (daily)

for season in season_list:
    cstats.plot_all(
        data=data["EURO-CORDEX_s"],
        var="c_bm",
        season=season,
        levels=cstats.colorbar_levels(4.5),
        ticks=cstats.colorbar_ticks(4.5),
    )

# ## Standing biomass (cumulative)

for season in season_list:
    cstats.plot_all(
        data=data["EURO-CORDEX_s"],
        var="bm",
        season=season,
        levels=cstats.colorbar_levels(450),
        ticks=cstats.colorbar_ticks(450),
    )

# ## Defoliation (senescence + abscission) (daily)

for season in season_list:
    cstats.plot_all(
        data=data["EURO-CORDEX_s"],
        var="sen_abs",
        season=season,
        levels=cstats.colorbar_levels(15),
        ticks=cstats.colorbar_ticks(15),
    )
