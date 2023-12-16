#!/usr/bin/env python
# coding: utf-8

# # Annual/overall stats - HiResIreland - Difference in (unbiased) standard deviation - historical and rcp45/rcp85

import importlib
# import libraries
from datetime import datetime, timezone

import climag.plot_stats as cstats

season_list = ["DJF", "MAM", "JJA", "SON"]

data = cstats.hist_rcp_stats_data(dataset="HiResIreland", stat="std")

importlib.reload(cstats)

# ## Total growth (daily)

cstats.plot_all(
    data=data["HiResIreland_a"],
    var="gro",
    season=None,
    levels=cstats.colorbar_levels(1.8),
    ticks=cstats.colorbar_ticks(1.8),
)

# ## Potential growth (daily)

cstats.plot_all(
    data=data["HiResIreland_a"],
    var="pgro",
    season=None,
    levels=cstats.colorbar_levels(4.5),
    ticks=cstats.colorbar_ticks(4.5),
)

# ## Total ingestion (daily)

cstats.plot_all(
    data=data["HiResIreland_a"],
    var="c_bm",
    season=None,
    levels=cstats.colorbar_levels(0.6),
    ticks=cstats.colorbar_ticks(0.6),
)

# ## Standing biomass (cumulative)

cstats.plot_all(
    data=data["HiResIreland_a"],
    var="bm",
    season=None,
    levels=cstats.colorbar_levels(90),
    ticks=cstats.colorbar_ticks(90),
)

# ## Defoliation (senescence + abscission) (daily)

cstats.plot_all(
    data=data["HiResIreland_a"],
    var="sen_abs",
    season=None,
    levels=cstats.colorbar_levels(4.5),
    ticks=cstats.colorbar_ticks(4.5),
)

# ## Total biomass consumption (ingested + harvested) (yearly total)

cstats.plot_all(
    data=data["HiResIreland_c"],
    var="c_bm_all",
    season=None,
    levels=cstats.colorbar_levels(450),
    ticks=cstats.colorbar_ticks(450),
)

print("Last updated:", datetime.now(tz=timezone.utc))
