#!/usr/bin/env python
# coding: utf-8

# # ModVege results - HiResIreland - (weighted) mean
#
# - Weighted means take into account the number of days in each month

# import libraries
from datetime import datetime, timezone
import climag.plot_stats as cstats

data = cstats.hist_rcp_stats_data(
    dataset="HiResIreland", stat="mean", diff=False
)

season_list = ["DJF", "MAM", "JJA", "SON"]

# ## Total growth (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="gro",
        season=season,
        levels=[0 + 9 * n for n in range(11)],
    )

# ## Potential growth (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="pgro",
        season=season,
        levels=[0 + 20 * n for n in range(11)],
    )

# ## Total ingestion (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="c_bm",
        season=season,
        levels=[0 + 3 * n for n in range(11)],
    )

# ## Standing biomass (cumulative)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="bm",
        season=season,
        levels=[0 + 300 * n for n in range(11)],
    )

# ## Senescence (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="sen",
        season=season,
        levels=[0 + 7.5 * n for n in range(11)],
    )

# ## Abscission (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="abs",
        season=season,
        levels=[0 + 3.6 * n for n in range(11)],
    )

# ## Ingested biomass (yearly total)

cstats.plot_all(
    data=data["HiResIreland_c"],
    var="i_bm",
    season=None,
    levels=[0 + 480 * n for n in range(11)],
)

# ## Harvested biomass (yearly total)

cstats.plot_all(
    data=data["HiResIreland_c"],
    var="h_bm",
    season=None,
    levels=[0 + 48 * n for n in range(11)],
)

print("Last updated:", datetime.now(tz=timezone.utc))
