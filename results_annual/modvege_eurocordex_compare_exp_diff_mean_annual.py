#!/usr/bin/env python
# coding: utf-8

# # Annual/overall stats - EURO-CORDEX - Difference in (weighted) mean - historical and rcp45/rcp85
#
# - Weighted means take into account the number of days in each month

import importlib
# import libraries
from datetime import datetime, timezone

import climag.plot_stats as cstats

season_list = ["DJF", "MAM", "JJA", "SON"]

data = cstats.hist_rcp_stats_data(
    dataset="EURO-CORDEX", stat="mean", annual=True
)

importlib.reload(cstats)

# ## Total growth (daily)

cstats.plot_all(
    data=data["EURO-CORDEX_s"],
    var="gro",
    season=None,
    levels=cstats.colorbar_levels(6),
    ticks=cstats.colorbar_ticks(6),
)

# ## Potential growth (daily)

cstats.plot_all(
    data=data["EURO-CORDEX_s"],
    var="pgro",
    season=None,
    levels=cstats.colorbar_levels(10),
    ticks=cstats.colorbar_ticks(10),
)

# ## Total ingestion (daily)

cstats.plot_all(
    data=data["EURO-CORDEX_s"],
    var="c_bm",
    season=None,
    levels=cstats.colorbar_levels(2.4),
    ticks=cstats.colorbar_ticks(2.4),
)

# ## Standing biomass (cumulative)

cstats.plot_all(
    data=data["EURO-CORDEX_s"],
    var="bm",
    season=None,
    levels=cstats.colorbar_levels(400),
    ticks=cstats.colorbar_ticks(400),
)

# ## Defoliation (senescence + abscission) (daily)

cstats.plot_all(
    data=data["EURO-CORDEX_s"],
    var="sen_abs",
    season=None,
    levels=cstats.colorbar_levels(7.5),
    ticks=cstats.colorbar_ticks(7.5),
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
