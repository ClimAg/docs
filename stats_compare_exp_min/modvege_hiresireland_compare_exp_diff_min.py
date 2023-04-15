#!/usr/bin/env python
# coding: utf-8

# # ModVege results - HiResIreland - Difference in min - historical and rcp45/rcp85

# import libraries
from datetime import datetime, timezone
import climag.plot_stats as cstats
import importlib

season_list = ["DJF", "MAM", "JJA", "SON"]

data = cstats.hist_rcp_stats_data(dataset="HiResIreland", stat="min")

importlib.reload(cstats)

# ## Total growth (daily)

for season in season_list:
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="gro",
        season=season,
        levels=cstats.colorbar_levels(24),
        ticks=cstats.colorbar_ticks(24),
    )

# ## Potential growth (daily)

for season in season_list:
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="pgro",
        season=season,
        levels=cstats.colorbar_levels(30),
        ticks=cstats.colorbar_ticks(30),
    )

# ## Total ingestion (daily)

for season in season_list:
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="c_bm",
        season=season,
        levels=cstats.colorbar_levels(24),
        ticks=cstats.colorbar_ticks(24),
    )

# ## Standing biomass (cumulative)

for season in season_list:
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="bm",
        season=season,
        levels=cstats.colorbar_levels(1200),
        ticks=cstats.colorbar_ticks(1200),
    )

# ## Defoliation (senescence + abscission) (daily)

for season in season_list:
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="sen_abs",
        season=season,
        levels=cstats.colorbar_levels(45),
        ticks=cstats.colorbar_ticks(45),
    )

# ## Total biomass consumption (ingested + harvested) (yearly total)

cstats.plot_all(
    data=data["HiResIreland_c"],
    var="c_bm_all",
    season=None,
    levels=cstats.colorbar_levels(1500),
    ticks=cstats.colorbar_ticks(1500),
)

print("Last updated:", datetime.now(tz=timezone.utc))
