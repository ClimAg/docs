#!/usr/bin/env python
# coding: utf-8

# # ModVege grass growth model (Jouven et al. 2006) with EURO-CORDEX data
#
# - Jouven, M., Carrère, P., and Baumont, R. (2006a). 'Model predicting
#   dynamics of biomass, structure and digestibility of herbage in managed
#   permanent pastures. 1. Model description', *Grass and Forage Science*,
#   vol. 61, no. 2, pp. 112-124. DOI:
#   [10.1111/j.1365-2494.2006.00515.x][Jouven1].
# - Jouven, M., Carrère, P., and Baumont, R. (2006b). 'Model predicting
#   dynamics of biomass, structure and digestibility of herbage in managed
#   permanent pastures. 2. Model evaluation', *Grass and Forage Science*,
#   vol. 61, no. 2, pp. 125-133. DOI:
#   [10.1111/j.1365-2494.2006.00517.x][Jouven2].
# - Chemin, Y. (2022). 'modvege', Python. [Online]. Available at
#   <https://github.com/YannChemin/modvege> (Accessed 6 September 2022).
#
# [Jouven1]: https://doi.org/10.1111/j.1365-2494.2006.00515.x
# [Jouven2]: https://doi.org/10.1111/j.1365-2494.2006.00517.x

import os
import glob
from datetime import datetime, timezone
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import xarray as xr
from dask.distributed import Client
import climag.plot_configs as cplt

print("Last updated:", datetime.now(tz=timezone.utc))

client = Client(n_workers=3, threads_per_worker=4, memory_limit="2GB")

client

DATA_DIR = os.path.join("data", "ModVege")

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries.gpkg")
# ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")
ie_bbox = gpd.read_file(
    GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE_BBOX_DIFF"
)

# met station coords
LON_VAL, LAT_VAL = -10.24333, 51.93806  # Valentia Observatory
LON_MPF, LAT_MPF = -8.26389, 52.16389  # Moorepark, Fermoy

# ## rcp45

data = xr.open_mfdataset(
    glob.glob(
        os.path.join(DATA_DIR, "EURO-CORDEX", "rcp45", "EC-EARTH", "*.nc")
    ),
    chunks="auto",
    decode_coords="all",
)

data

# remove the spin-up year
data = data.sel(time=slice("2041", "2070"))

# cumulative biomass
data["c_bm"].attrs["long_name"] = "Net biomass production"

# ### Annual averages

cplt.plot_averages(
    data=data,
    var="gro",
    averages="year",
    boundary_data=ie_bbox,
    cbar_levels=12,
)

# ### Monthly averages

cplt.plot_averages(
    data=data,
    var="gro",
    averages="month",
    boundary_data=ie_bbox,
    cbar_levels=[0 + 10 * n for n in range(16)],
)

for var in ["gro", "bm", "pgro", "i_bm", "h_bm", "c_bm", "aet"]:
    cplt.plot_averages(
        data=data,
        var=var,
        averages="month",
        boundary_data=ie_bbox,
        cbar_levels=12,
    )

# ### Seasonal averages

for var in ["gro", "pgro", "bm", "aet"]:
    cplt.plot_averages(
        data=data,
        var=var,
        averages="season",
        boundary_data=ie_bbox,
        cbar_levels=12,
    )

# ### Point subset

# #### Valentia Observatory

cds = cplt.rotated_pole_point(data=data, lon=LON_VAL, lat=LAT_VAL)
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest").sel(
    time=slice("2054", "2056")
)

data_ie_df = pd.DataFrame({"time": data_ie["time"]})
for var in data_ie.data_vars:
    data_ie_df[var] = data_ie[var]

data_ie_df.set_index("time", inplace=True)
data_ie_df = data_ie_df[["pgro", "gro", "h_bm", "i_bm", "bm", "c_bm"]]

# configure plot title
plot_title = []
for var in list(data_ie_df):
    plot_title.append(
        f"{data_ie[var].attrs['long_name']} [{data_ie[var].attrs['units']}]"
    )

data_ie_df.plot(
    subplots=True,
    layout=(3, 2),
    figsize=(13, 8),
    legend=False,
    xlabel="",
    title=plot_title,
)

plt.tight_layout()
plt.show()

cds = cplt.rotated_pole_point(data=data, lon=LON_VAL, lat=LAT_VAL)
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest").sel(
    time=slice("2054", "2056")
)

data_ie_df = pd.DataFrame({"time": data_ie["time"]})

# configure plot title
plot_title = []

for var in data_ie.data_vars:
    data_ie_df[var] = data_ie[var]
    plot_title.append(
        f"{data_ie[var].attrs['long_name']} [{data_ie[var].attrs['units']}]"
    )

data_ie_df.set_index("time", inplace=True)

data_ie_df.plot(
    subplots=True,
    layout=(5, 3),
    figsize=(15, 11),
    legend=False,
    xlabel="",
    title=plot_title,
)

plt.tight_layout()
plt.show()

# #### Moorepark

cds = cplt.rotated_pole_point(data=data, lon=LON_MPF, lat=LAT_MPF)
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest").sel(
    time=slice("2054", "2056")
)

data_ie_df = pd.DataFrame({"time": data_ie["time"]})
for var in data_ie.data_vars:
    data_ie_df[var] = data_ie[var]

data_ie_df.set_index("time", inplace=True)
data_ie_df = data_ie_df[["pgro", "gro", "i_bm", "h_bm", "bm", "c_bm"]]

# configure plot title
plot_title = []
for var in list(data_ie_df):
    plot_title.append(
        f"{data_ie[var].attrs['long_name']} [{data_ie[var].attrs['units']}]"
    )

data_ie_df.plot(
    subplots=True,
    layout=(3, 2),
    figsize=(13, 8),
    legend=False,
    xlabel="",
    title=plot_title,
)

plt.tight_layout()
plt.show()

cds = cplt.rotated_pole_point(data=data, lon=LON_MPF, lat=LAT_MPF)
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest").sel(
    time=slice("2054", "2056")
)

data_ie_df = pd.DataFrame({"time": data_ie["time"]})

# configure plot title
plot_title = []

for var in data_ie.data_vars:
    data_ie_df[var] = data_ie[var]
    plot_title.append(
        f"{data_ie[var].attrs['long_name']} [{data_ie[var].attrs['units']}]"
    )

data_ie_df.set_index("time", inplace=True)

data_ie_df.plot(
    subplots=True,
    layout=(5, 3),
    figsize=(15, 11),
    legend=False,
    xlabel="",
    title=plot_title,
)

plt.tight_layout()
plt.show()

data_ie_y = data_ie.sel(time=slice("2054", "2056"))

data_ie_df = pd.DataFrame({"time": data_ie_y["time"]})

for var in data_ie_y.data_vars:
    data_ie_df[var] = data_ie_y[var]

data_ie_df.set_index("time", inplace=True)
data_ie_df = data_ie_df[["gro"]]

# resample to weekly
data_ie_df = data_ie_df.resample("W-MON").mean()

data_ie_df.reset_index(inplace=True)
mn = data_ie_df.rolling(3, center=True, on="time")["gro"].mean()
data_ie_df["outlier"] = data_ie_df["gro"].sub(mn).abs().gt(10)
data_ie_df["moving_avg"] = mn
data_ie_df.set_index("time", inplace=True)

axs = data_ie_df.plot(y="gro", figsize=(12, 5), xlabel="", label="growth")
data_ie_df.plot(y="moving_avg", ax=axs, color="orange", zorder=1)
data_ie_df[data_ie_df["outlier"] is True].plot(
    y="gro",
    ax=axs,
    marker="*",
    linewidth=0.0,
    color="crimson",
    label="outlier",
)
plt.xlabel("")
plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
plt.tight_layout()
plt.show()
