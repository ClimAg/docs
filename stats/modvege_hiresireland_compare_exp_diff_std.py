#!/usr/bin/env python
# coding: utf-8

# # ModVege results - HiResIreland - Difference in (unbiased) standard deviation - historical and rcp45/rcp85

# import libraries
from datetime import datetime, timezone
import climag.plot_stats as cstats

data = cstats.hist_rcp_stats_data(dataset="HiResIreland", stat="std")

season_list = ["DJF", "MAM", "JJA", "SON"]

# ## Total growth (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="gro",
        season=season,
        levels=[-12 + 0.96 * n for n in range(26)],
        ticks=[-12 + 4 * n for n in range(7)],
    )

# ## Potential growth (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="pgro",
        season=season,
        levels=[-24 + 1.92 * n for n in range(26)],
        ticks=[-24 + 8 * n for n in range(7)],
    )

# ## Total ingestion (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="c_bm",
        season=season,
        levels=[-4.5 + 0.36 * n for n in range(26)],
        ticks=[-4.5 + 1.5 * n for n in range(7)],
    )

# ## Standing biomass (cumulative)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="bm",
        season=season,
        levels=[-450 + 36 * n for n in range(26)],
        ticks=[-450 + 150 * n for n in range(7)],
    )

# ## Senescence (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="sen",
        season=season,
        levels=[-12 + 0.96 * n for n in range(26)],
        ticks=[-12 + 4 * n for n in range(7)],
    )

# ## Abscission (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["HiResIreland_s"],
        var="abs",
        season=season,
        levels=[-6 + 0.48 * n for n in range(26)],
        ticks=[-6 + 2 * n for n in range(7)],
    )

# ## Ingested biomass (yearly total)

cstats.plot_all(
    data=data["HiResIreland_c"],
    var="i_bm",
    season=None,
    levels=[-300 + 24 * n for n in range(26)],
    ticks=[-300 + 100 * n for n in range(7)],
)

# ## Harvested biomass (yearly total)

cstats.plot_all(
    data=data["HiResIreland_c"],
    var="h_bm",
    season=None,
    levels=[-300 + 24 * n for n in range(26)],
    ticks=[-300 + 100 * n for n in range(7)],
)

print("Last updated:", datetime.now(tz=timezone.utc))
