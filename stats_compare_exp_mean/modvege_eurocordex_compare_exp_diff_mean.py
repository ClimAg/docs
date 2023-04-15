#!/usr/bin/env python
# coding: utf-8

# # ModVege results - EURO-CORDEX - Difference in (weighted) mean - historical and rcp45/rcp85
#
# - Weighted means take into account the number of days in each month

# import libraries
from datetime import datetime, timezone
import climag.plot_stats as cstats
import importlib

season_list = ["DJF", "MAM", "JJA", "SON"]

data = cstats.hist_rcp_stats_data(dataset="EURO-CORDEX", stat="mean")

importlib.reload(cstats)

# ## Total growth (daily)

for season in season_list:
    cstats.plot_all(
        data=data["EURO-CORDEX_s"],
        var="gro",
        season=season,
        levels=cstats.colorbar_levels(24),
        ticks=cstats.colorbar_ticks(24),
    )

# ## Potential growth (daily)

for season in season_list:
    cstats.plot_all(
        data=data["EURO-CORDEX_s"],
        var="pgro",
        season=season,
        levels=cstats.colorbar_levels(30),
        ticks=cstats.colorbar_ticks(30),
    )

# ## Total ingestion (daily)

for season in season_list:
    cstats.plot_all(
        data=data["EURO-CORDEX_s"],
        var="c_bm",
        season=season,
        levels=cstats.colorbar_levels(7.5),
        ticks=cstats.colorbar_ticks(7.5),
    )

# ## Standing biomass (cumulative)

for season in season_list:
    cstats.plot_all(
        data=data["EURO-CORDEX_s"],
        var="bm",
        season=season,
        levels=cstats.colorbar_levels(900),
        ticks=cstats.colorbar_ticks(900),
    )

# ## Defoliation (senescence + abscission) (daily)

for season in season_list:
    cstats.plot_all(
        data=data["EURO-CORDEX_s"],
        var="sen_abs",
        season=season,
        levels=cstats.colorbar_levels(30),
        ticks=cstats.colorbar_ticks(30),
    )

# ## Total biomass consumption (ingested + harvested) (yearly total)

cstats.plot_all(
    data=data["EURO-CORDEX_c"],
    var="c_bm_all",
    season=None,
    levels=cstats.colorbar_levels(750),
    ticks=cstats.colorbar_ticks(750),
)

print("Last updated:", datetime.now(tz=timezone.utc))
