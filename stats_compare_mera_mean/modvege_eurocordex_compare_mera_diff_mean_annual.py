#!/usr/bin/env python
# coding: utf-8

# # Annual/overall stats - EURO-CORDEX - Difference in (weighted) mean - historical and observational (MÉRA)
#
# - Weighted means take into account the number of days in each month

# import libraries
from datetime import datetime, timezone
import climag.plot_stats as cstats
import importlib

season_list = ["DJF", "MAM", "JJA", "SON"]

data = cstats.hist_obs_diff(stat="mean", dataset="EURO-CORDEX")

importlib.reload(cstats)

# ## Total growth (daily)

data["MERA_s_diff"]

data["MERA_c_diff"]

data["MERA_a_diff"]

data["MERA_a_diff"].isel(model=0)["bm"].plot()

# cstats.plot_obs_diff_all(
#     data=data["MERA_a_diff"], var="gro", season=None,
#     # levels=cstats.colorbar_levels(6),
#     # ticks=cstats.colorbar_ticks(6)
# )

# ## Potential growth (daily)

# cstats.plot_obs_diff_all(
#     data=data["MERA_a_diff"], var="pgro", season=None,
#     # levels=cstats.colorbar_levels(75),
#     # ticks=cstats.colorbar_ticks(75)
# )

# ## Total ingestion (daily)

# cstats.plot_obs_diff_all(
#     data=data["MERA_a_diff"], var="c_bm", season=None,
#     # levels=cstats.colorbar_levels(12.5),
#     # ticks=cstats.colorbar_ticks(12.5)
# )

# ## Standing biomass (cumulative)

# cstats.plot_obs_diff_all(
#     data=data["MERA_a_diff"], var="bm", season=None,
#     # levels=cstats.colorbar_levels(2500),
#     # ticks=cstats.colorbar_ticks(2500)
# )

# ## Defoliation (senescence + abscission) (daily)

cstats.plot_obs_diff_all(
    data=data["MERA_a_diff"],
    var="sen_abs",
    season=None,
    # levels=cstats.colorbar_levels(80),
    # ticks=cstats.colorbar_ticks(80)
)

# ## Total biomass consumption (ingested + harvested) (yearly total)

cstats.plot_obs_diff_all(
    data=data["MERA_c_diff"],
    var="c_bm_all",
    season=None,
    levels=cstats.colorbar_levels(3000),
    ticks=cstats.colorbar_ticks(3000),
)

print("Last updated:", datetime.now(tz=timezone.utc))
