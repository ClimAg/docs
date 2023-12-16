#!/usr/bin/env python
# coding: utf-8

# # Annual/overall stats - EURO-CORDEX - Difference in minimum - historical and rcp45/rcp85

import importlib
# import libraries
from datetime import datetime, timezone

import climag.plot_stats as cstats

season_list = ["DJF", "MAM", "JJA", "SON"]

data = cstats.hist_rcp_stats_data(
    dataset="EURO-CORDEX", stat="min", annual=True
)

importlib.reload(cstats)

# ## Total growth (daily)

cstats.plot_all(data=data["EURO-CORDEX_s"], var="gro", season=None)

# ## Potential growth (daily)

cstats.plot_all(
    data=data["EURO-CORDEX_s"],
    var="pgro",
    season=None,
    levels=cstats.colorbar_levels(1.2),
    ticks=cstats.colorbar_ticks(1.2),
)

# ## Total ingestion (daily)

cstats.plot_all(data=data["EURO-CORDEX_s"], var="c_bm", season=None)

# ## Standing biomass (cumulative)

cstats.plot_all(
    data=data["EURO-CORDEX_s"],
    var="bm",
    season=None,
    levels=cstats.colorbar_levels(150),
    ticks=cstats.colorbar_ticks(150),
)

# ## Defoliation (senescence + abscission) (daily)

cstats.plot_all(
    data=data["EURO-CORDEX_s"],
    var="sen_abs",
    season=None,
    levels=cstats.colorbar_levels(0.06),
    ticks=cstats.colorbar_ticks(0.06),
)

# ## Total biomass consumption (ingested + harvested) (yearly total)

cstats.plot_all(
    data=data["EURO-CORDEX_c"],
    var="c_bm_all",
    season=None,
    levels=cstats.colorbar_levels(1500),
    ticks=cstats.colorbar_ticks(1500),
)

print("Last updated:", datetime.now(tz=timezone.utc))
