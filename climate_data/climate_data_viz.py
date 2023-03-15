#!/usr/bin/env python
# coding: utf-8

# # Visualising climate model datasets

# import libraries
import os
import glob
import itertools
import numpy as np
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
from dask.distributed import Client
import climag.plot_configs as cplt
import climag.plot_facet_maps as cfacet

print("Last updated:", datetime.now(tz=timezone.utc))

client = Client(n_workers=2, threads_per_worker=4, memory_limit="3GB")

client

# Moorepark met station coords
LON, LAT = -8.26389, 52.16389

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries.gpkg")
ie_bbox = gpd.read_file(GPKG_BOUNDARY, layer="ne_10m_land_2157_IE_BBOX_DIFF")

datasets = {}

for exp, model, data in itertools.product(
    ["historical", "rcp45", "rcp85"],
    ["CNRM-CM5", "EC-EARTH", "HadGEM2-ES", "MPI-ESM-LR"],
    ["EURO-CORDEX", "HiResIreland"],
):
    # auto-rechunking may cause NotImplementedError with object dtype
    # where it will not be able to estimate the size in bytes of object data
    if model == "HadGEM2-ES":
        CHUNKS = 300
    else:
        CHUNKS = "auto"

    datasets[f"{data}_{model}_{exp}"] = xr.open_dataset(
        glob.glob(
            os.path.join("data", data, "IE", f"*{data}*{model}*{exp}*.nc")
        )[0],
        chunks=CHUNKS,
        decode_coords="all",
    )

    # convert HadGEM2-ES data back to 360-day calendar
    # this ensures that the correct weighting is applied when calculating
    # the weighted average
    if model == "HadGEM2-ES":
        datasets[f"{data}_{model}_{exp}"] = datasets[
            f"{data}_{model}_{exp}"
        ].convert_calendar("360_day", align_on="year")

# remove spin-up year
for key in datasets.keys():
    if "historical" in key:
        datasets[key] = datasets[key].sel(time=slice("1976", "2005"))
    else:
        datasets[key] = datasets[key].sel(time=slice("2041", "2070"))
    # # normalise to keep only date in time
    # datasets[key]["time"] = datasets[key].indexes["time"].normalize()

varlist = ["PAR", "PET", "PP", "T"]

# ## Box plots

data_all = cplt.boxplot_data(
    datasets=datasets, varlist=varlist, lonlat=(LON, LAT)
)

for var in varlist:
    cplt.boxplot_all(
        data=data_all[var],
        var=var,
        title=(
            datasets["EURO-CORDEX_EC-EARTH_rcp45"][var].attrs["long_name"]
            + f" [{datasets['EURO-CORDEX_EC-EARTH_rcp45'][var].attrs['units']}]"
            f" at Moorepark ({LON}, {LAT})"
        ),
    )

# ## Histograms

c

# ## Seasonal maps - hist/rcp diff

# ### hist/rcp45

for var in varlist:
    cfacet.plot_season_diff_hist_rcp(
        data=(
            datasets["EURO-CORDEX_EC-EARTH_historical"],
            datasets["EURO-CORDEX_EC-EARTH_rcp45"],
        ),
        var=var,
        boundary_data=ie_bbox,
        stat="mean",
    )

# ### hist/rcp85

for var in varlist:
    cfacet.plot_season_diff_hist_rcp(
        data=(
            datasets["EURO-CORDEX_EC-EARTH_historical"],
            datasets["EURO-CORDEX_EC-EARTH_rcp85"],
        ),
        var=var,
        boundary_data=ie_bbox,
        stat="mean",
    )

# ## Seasonal maps

# ### Mean

# #### Weighted vs. unweighted mean

cfacet.plot_season_diff(
    data=datasets["EURO-CORDEX_EC-EARTH_rcp45"],
    var="PP",
    boundary_data=ie_bbox,
    stat="mean",
)

# #### Mean

cfacet.plot_seasonal(
    data=datasets["EURO-CORDEX_EC-EARTH_rcp45"],
    # cbar_levels=[2 + 0.25 * n for n in range(56)],
    boundary_data=ie_bbox,
    stat="mean",
    var="PP",
    contour=True,
)

cfacet.plot_seasonal(
    data=datasets["HiResIreland_EC-EARTH_rcp45"],
    # cbar_levels=[2 + 0.25 * n for n in range(56)],
    boundary_data=ie_bbox,
    stat="mean",
    var="PP",
    contour=True,
)

# ### Quantiles

# #### Median

cfacet.plot_seasonal(
    data=datasets["HiResIreland_EC-EARTH_rcp45"],
    boundary_data=ie_bbox,
    stat="median",
    var="PP",
    contour=True,
)

# #### 90th percentile

cfacet.plot_seasonal(
    data=datasets["HiResIreland_EC-EARTH_rcp45"],
    boundary_data=ie_bbox,
    stat="0.9q",
    var="PP",
    contour=True,
)

# #### 10th percentile

cfacet.plot_seasonal(
    data=datasets["HiResIreland_EC-EARTH_rcp45"],
    boundary_data=ie_bbox,
    stat="0.1q",
    var="PP",
    contour=True,
)

# ### Standard deviation

# #### Unbised vs. biased SD

cfacet.plot_season_diff(
    datasets["HiResIreland_EC-EARTH_rcp45"],
    var="PP",
    boundary_data=ie_bbox,
    stat="std",
)

# #### SD

cfacet.plot_seasonal(
    data=datasets["HiResIreland_EC-EARTH_rcp45"],
    boundary_data=ie_bbox,
    stat="std",
    var="PP",
    contour=True,
)

# ### Max and min

# #### Max

cfacet.plot_seasonal(
    data=datasets["EURO-CORDEX_EC-EARTH_rcp45"],
    boundary_data=ie_bbox,
    stat="max",
    var="PP",
    contour=True,
)

# #### Min

cfacet.plot_seasonal(
    data=datasets["HiResIreland_EC-EARTH_rcp45"],
    boundary_data=ie_bbox,
    stat="min",
    var="T",
    contour=True,
)

# ### Selecting seasonal data

seasonal_data = datasets["EURO-CORDEX_EC-EARTH_rcp45"].sel(
    time=datasets["EURO-CORDEX_EC-EARTH_rcp45"]["time.season"] == "JJA"
)

seasonal_data

# ## Time series

# using Moorepark met station coordinates
cds = cplt.rotated_pole_point(
    data=datasets["EURO-CORDEX_EC-EARTH_rcp45"], lon=LON, lat=LAT
)

data_ie = datasets["EURO-CORDEX_EC-EARTH_rcp45"].sel(
    {"rlon": cds[0], "rlat": cds[1]}, method="nearest"
)

data_ie

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
    layout=(4, 1),
    figsize=(12, 11),
    legend=False,
    xlabel="",
    title=plot_title,
    linewidth=0.5,
)

plt.tight_layout()
plt.show()

data_ie = data_ie.sel(time=slice("1997", "1999"))

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
    layout=(4, 1),
    figsize=(12, 11),
    legend=False,
    xlabel="",
    title=plot_title,
)

plt.tight_layout()
plt.show()

# ### Box plots

data_ie = (
    datasets["EURO-CORDEX_EC-EARTH_rcp45"]
    .sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")
    .sel(time=slice("1976", "2005"))
)

data_ie_df = pd.DataFrame({"time": data_ie["time"]})
for var in data_ie.data_vars:
    data_ie_df[var] = data_ie[var]
data_ie_df.set_index("time", inplace=True)

fig, axs = plt.subplots(2, 2, figsize=(12, 4))
for ax, var in zip(axs.flat, data_ie.data_vars):
    data_ie_df.plot.box(
        column=var,
        vert=False,
        showmeans=True,
        ax=ax,
        patch_artist=True,
        color={
            "medians": "Crimson",
            "whiskers": "DarkSlateGrey",
            "caps": "DarkSlateGrey",
        },
        boxprops={"facecolor": "Lavender", "color": "DarkSlateGrey"},
        meanprops={
            "markeredgecolor": "DarkSlateGrey",
            "marker": "d",
            "markerfacecolor": (1, 1, 0, 0),  # transparent
        },
        flierprops={
            "alpha": 0.5,
            "markeredgecolor": "LightSteelBlue",
            "zorder": 1,
        },
    )
    ax.set_title(
        f"{data_ie[var].attrs['long_name']} [{data_ie[var].attrs['units']}]"
    )
    ax.set(yticklabels=[])
plt.tight_layout()
plt.show()

data_ie_df = data_ie_df[["PP"]].resample("A").sum()
data_ie_df.set_index(data_ie_df.index.year, inplace=True)

data_ie_df.plot.bar(figsize=(12, 4), legend=False, xlabel="")
plt.title("Total precipitation [mm year⁻¹]")
plt.tight_layout()
plt.show()

data_ie_df.diff().plot.hist(
    bins=15, edgecolor="darkslategrey", legend=False, alpha=0.75, hatch="///"
)
plt.show()

data_ie_df.plot.hist(
    bins=15, edgecolor="darkslategrey", legend=False, alpha=0.75, hatch="///"
)
plt.show()
