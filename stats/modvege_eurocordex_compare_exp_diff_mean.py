#!/usr/bin/env python
# coding: utf-8

# # ModVege results - EURO-CORDEX - Difference in (weighted) mean - historical and rcp45/rcp85
#
# - Weighted means take into account the number of days in each month

# import libraries
from datetime import datetime, timezone
import climag.plot_stats as cstats

data = cstats.hist_rcp_stats_data(dataset="EURO-CORDEX", stat="mean")

season_list = ["DJF", "MAM", "JJA", "SON"]

# ## Total growth (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["EURO-CORDEX_s"],
        var="gro",
        season=season,
        levels=[-24 + 1.92 * n for n in range(26)],
        ticks=[-24 + 8 * n for n in range(7)],
    )

# ## Potential growth (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["EURO-CORDEX_s"],
        var="pgro",
        season=season,
        levels=[-30 + 2.4 * n for n in range(26)],
        ticks=[-30 + 10 * n for n in range(7)],
    )

# ## Total ingestion (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["EURO-CORDEX_s"],
        var="c_bm",
        season=season,
        levels=[-7.5 + 0.6 * n for n in range(26)],
        ticks=[-7.5 + 2.5 * n for n in range(7)],
    )

# ## Standing biomass (cumulative)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["EURO-CORDEX_s"],
        var="bm",
        season=season,
        levels=[-900 + 72 * n for n in range(26)],
        ticks=[-900 + 300 * n for n in range(7)],
    )

# ## Senescence (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["EURO-CORDEX_s"],
        var="sen",
        season=season,
        levels=[-15 + 1.2 * n for n in range(26)],
        ticks=[-15 + 5 * n for n in range(7)],
    )

# ## Abscission (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    cstats.plot_all(
        data=data["EURO-CORDEX_s"],
        var="abs",
        season=season,
        levels=[-15 + 1.2 * n for n in range(26)],
        ticks=[-15 + 5 * n for n in range(7)],
    )

# ## Ingested biomass (yearly total)

cstats.plot_all(
    data=data["EURO-CORDEX_c"],
    var="i_bm",
    season=None,
    levels=[-750 + 60 * n for n in range(26)],
    ticks=[-750 + 250 * n for n in range(7)],
)

# ## Harvested biomass (yearly total)

cstats.plot_all(
    data=data["EURO-CORDEX_c"],
    var="h_bm",
    season=None,
    levels=[-450 + 36 * n for n in range(26)],
    ticks=[-450 + 150 * n for n in range(7)],
)

print("Last updated:", datetime.now(tz=timezone.utc))
