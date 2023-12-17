#!/usr/bin/env python
# coding: utf-8

# # Annual/overall stats - EURO-CORDEX - Difference in maximum - historical and rcp45/rcp85

import importlib
from datetime import datetime, timezone

import climag.plot_stats as cstats

season_list = ["DJF", "MAM", "JJA", "SON"]

data = cstats.hist_rcp_stats_data(
    dataset="EURO-CORDEX", stat="max", annual=True
)

importlib.reload(cstats)

# ## Total growth (daily)

cstats.plot_all(
    data=data["EURO-CORDEX_s"],
    var="gro",
    season=None,
    levels=cstats.colorbar_levels(12),
    ticks=cstats.colorbar_ticks(12),
)

# ## Potential growth (daily)

cstats.plot_all(
    data=data["EURO-CORDEX_s"],
    var="pgro",
    season=None,
    levels=cstats.colorbar_levels(45),
    ticks=cstats.colorbar_ticks(45),
)

# ## Total ingestion (daily)

cstats.plot_all(data=data["EURO-CORDEX_s"], var="c_bm", season=None)

# ## Standing biomass (cumulative)

cstats.plot_all(
    data=data["EURO-CORDEX_s"],
    var="bm",
    season=None,
    levels=cstats.colorbar_levels(750),
    ticks=cstats.colorbar_ticks(750),
)

# ## Defoliation (senescence + abscission) (daily)

cstats.plot_all(
    data=data["EURO-CORDEX_s"],
    var="sen_abs",
    season=None,
    levels=cstats.colorbar_levels(60),
    ticks=cstats.colorbar_ticks(60),
)

# ## Total biomass consumption (ingested + harvested) (yearly total)

cstats.plot_all(
    data=data["EURO-CORDEX_c"],
    var="c_bm_all",
    season=None,
    levels=cstats.colorbar_levels(900),
    ticks=cstats.colorbar_ticks(900),
)
