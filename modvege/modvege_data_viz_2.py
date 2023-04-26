#!/usr/bin/env python
# coding: utf-8

# # Visualising ModVege results

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

BASE_DIR = os.path.join("data", "ModVege", "EURO-CORDEX")
TEMP_DIR = os.path.join(BASE_DIR, "stats")
os.makedirs(TEMP_DIR, exist_ok=True)

exp, model = "rcp45", "EC-EARTH"

# ## Use CDO to calculate seasonal mean

# combine outputs into one
os.system(
    "cdo mergetime "
    + " ".join(glob.glob(os.path.join(BASE_DIR, exp, model, "*.nc")))
    + " "
    + os.path.join(
        TEMP_DIR, f"modvege_IE_EURO-CORDEX_RCA4_{model}_{exp}_merged.nc"
    )
)

# ### Unweighted

# calculate seasonal mean
os.system(
    "cdo yseasmean "
    + os.path.join(
        TEMP_DIR, f"modvege_IE_EURO-CORDEX_RCA4_{model}_{exp}_merged.nc"
    )
    + " "
    + os.path.join(
        TEMP_DIR, f"modvege_IE_EURO-CORDEX_RCA4_{model}_{exp}_seasmean.nc"
    )
)

data_cdo = xr.open_dataset(
    os.path.join(
        TEMP_DIR, f"modvege_IE_EURO-CORDEX_RCA4_{model}_{exp}_seasmean.nc"
    ),
    decode_coords="all",
    chunks="auto",
)

# add season coordinate
# data_cdo = data_cdo.assign_coords(season=data_cdo["time"].dt.season)
data_cdo = data_cdo.groupby("time.season").mean()
data_cdo = data_cdo.reindex(season=["DJF", "MAM", "JJA", "SON"])

data_cdo

var = "gro"
plot_transform = cplt.rotated_pole_transform(data_cdo)
cmap = cplt.colormap_configs(var)

fig = data_cdo[var].plot.contourf(
    x="rlon",
    y="rlat",
    col="season",
    # col_wrap=columns_cbar_aspect[0],
    cmap=cmap,
    robust=True,
    cbar_kwargs={
        # "aspect": columns_cbar_aspect[1],
        "label": (
            f"{data_cdo[var].attrs['long_name']}\n"
            f"[{data_cdo[var].attrs['units']}]"
        )
    },
    transform=plot_transform,
    subplot_kws={"projection": cplt.plot_projection},
    # levels=cbar_levels,
    xlim=(-1.9, 1.6),
    ylim=(-2.1, 2.1),
    aspect=0.9,
)

for i, axis in enumerate(fig.axs.flat):
    ie_bbox.to_crs(cplt.plot_projection).plot(
        ax=axis, color="white", edgecolor="darkslategrey", linewidth=0.5
    )
    axis.set_title(data_cdo["season"][i].values)

plt.show()

# ### Weighted

# calculate seasonal mean
os.system(
    "cdo ymonmean "
    + os.path.join(
        TEMP_DIR, f"modvege_IE_EURO-CORDEX_RCA4_{model}_{exp}_merged.nc"
    )
    + " "
    + os.path.join(
        TEMP_DIR,
        f"modvege_IE_EURO-CORDEX_RCA4_{model}_{exp}_wseasmean_temp.nc",
    )
)

for m, s in zip(
    ("12,1,2", "3,4,5", "6,7,8", "9,10,11"), ("djf", "mam", "jja", "son")
):
    os.system(
        f"cdo selmon,{m} "
        + os.path.join(
            TEMP_DIR,
            f"modvege_IE_EURO-CORDEX_RCA4_{model}_{exp}_wseasmean_temp.nc",
        )
        + " "
        + os.path.join(
            TEMP_DIR,
            f"modvege_IE_EURO-CORDEX_RCA4_{model}_{exp}_{s}wseasmean_temp.nc",
        )
    )

    os.system(
        "cdo yearmonmean "
        + os.path.join(
            TEMP_DIR,
            f"modvege_IE_EURO-CORDEX_RCA4_{model}_{exp}_{s}wseasmean_temp.nc",
        )
        + " "
        + os.path.join(
            TEMP_DIR,
            f"modvege_IE_EURO-CORDEX_RCA4_{model}_{exp}_{s}wseasmean.nc",
        )
    )

data_cw = xr.open_mfdataset(
    glob.glob(
        os.path.join(
            TEMP_DIR,
            f"modvege_IE_EURO-CORDEX_RCA4_{model}_{exp}_*wseasmean.nc",
        )
    ),
    decode_coords="all",
    chunks="auto",
)

# add season coordinate
data_cw = data_cw.groupby("time.season").mean()
data_cw = data_cw.reindex(season=["DJF", "MAM", "JJA", "SON"])

data_cw

var = "gro"
plot_transform = cplt.rotated_pole_transform(data_cw)
cmap = cplt.colormap_configs(var)

fig = data_cw[var].plot.contourf(
    x="rlon",
    y="rlat",
    col="season",
    # col_wrap=columns_cbar_aspect[0],
    cmap=cmap,
    robust=True,
    cbar_kwargs={
        # "aspect": columns_cbar_aspect[1],
        "label": (
            f"{data_cw[var].attrs['long_name']}\n"
            f"[{data_cw[var].attrs['units']}]"
        )
    },
    transform=plot_transform,
    subplot_kws={"projection": cplt.plot_projection},
    # levels=cbar_levels,
    xlim=(-1.9, 1.6),
    ylim=(-2.1, 2.1),
    aspect=0.9,
)

for i, axis in enumerate(fig.axs.flat):
    ie_bbox.to_crs(cplt.plot_projection).plot(
        ax=axis, color="white", edgecolor="darkslategrey", linewidth=0.5
    )
    axis.set_title(data_cw["season"][i].values)

plt.show()

# ## Use Xarray to calculate seasonal mean

data_xr = xr.open_dataset(
    os.path.join(
        TEMP_DIR, f"modvege_IE_EURO-CORDEX_RCA4_{model}_{exp}_merged.nc"
    ),
    decode_coords="all",
    chunks="auto",
)

# ### Weighted 1

weights = (
    data_xr.time.dt.days_in_month.groupby(f"time.season")
    / data_xr.time.dt.days_in_month.groupby(f"time.season").sum()
)

weights

set(weights.values)

data_w = {}
for seas in ["DJF", "MAM", "JJA", "SON"]:
    _data_xr = data_xr.sel(time=data_xr["time.season"] == seas)
    _weights = weights.sel(time=weights["time.season"] == seas)
    _data_xr.assign_coords(season=_data_xr["time"].dt.season)
    _data_xr = _data_xr.weighted(_weights)
    _data_xr = _data_xr.mean(dim="time")
    _data_xr = _data_xr.assign_coords(season=seas)
    data_w[seas] = _data_xr.expand_dims(dim="season")
    # data_w[seas] = _data_xr.copy()

data_w_all = xr.combine_by_coords(
    [data_w["DJF"], data_w["MAM"], data_w["JJA"], data_w["SON"]]
)
data_w_all = data_w_all.reindex(season=["DJF", "MAM", "JJA", "SON"])

data_w_all.rio.write_crs(data_xr.rio.crs, inplace=True)

data_w_all.rio.crs

var = "gro"
data_w_all[var].plot.contourf(
    x="rlon",
    y="rlat",
    col="season",
    cmap=cplt.colormap_configs(var),
    robust=True,
    transform=cplt.rotated_pole_transform(data_xr),
    subplot_kws={"projection": cplt.plot_projection},
    xlim=(-1.9, 1.6),
    ylim=(-2.1, 2.1),
)
plt.show()

# ### Weighted

data_xrm = cplt.weighted_average(data=data_xr, averages="season")

# sort seasons, reassign vars and crs
data_xrm = data_xrm.reindex(season=["DJF", "MAM", "JJA", "SON"])
for var in data_xrm.data_vars:
    data_xrm[var].attrs = data_xr[var].attrs
data_xrm.rio.write_crs(data_xr.rio.crs, inplace=True)

var = "gro"
plot_transform = cplt.rotated_pole_transform(data_xrm)
cmap = cplt.colormap_configs(var)

fig = data_xrm[var].plot.contourf(
    x="rlon",
    y="rlat",
    col="season",
    # col_wrap=columns_cbar_aspect[0],
    cmap=cmap,
    robust=True,
    cbar_kwargs={
        # "aspect": columns_cbar_aspect[1],
        "label": (
            f"{data_xrm[var].attrs['long_name']}\n"
            f"[{data_xrm[var].attrs['units']}]"
        )
    },
    transform=plot_transform,
    subplot_kws={"projection": cplt.plot_projection},
    # levels=cbar_levels,
    xlim=(-1.9, 1.6),
    ylim=(-2.1, 2.1),
    aspect=0.9,
)

for i, axis in enumerate(fig.axs.flat):
    ie_bbox.to_crs(cplt.plot_projection).plot(
        ax=axis, color="white", edgecolor="darkslategrey", linewidth=0.5
    )
    axis.set_title(data_xrm["season"][i].values)

plt.show()

var = "gro"
plot_transform = cplt.rotated_pole_transform(data_xrm)
cmap = cplt.colormap_configs(var)

fig = data_xrm[var].plot.contourf(
    x="rlon",
    y="rlat",
    col="season",
    # col_wrap=columns_cbar_aspect[0],
    cmap=cmap,
    robust=True,
    cbar_kwargs={
        # "aspect": columns_cbar_aspect[1],
        "label": (
            f"{data_xrm[var].attrs['long_name']}\n"
            f"[{data_xrm[var].attrs['units']}]"
        )
    },
    transform=plot_transform,
    subplot_kws={"projection": cplt.plot_projection},
    # levels=cbar_levels,
    xlim=(-1.9, 1.6),
    ylim=(-2.1, 2.1),
    aspect=0.9,
)

for i, axis in enumerate(fig.axs.flat):
    ie_bbox.to_crs(cplt.plot_projection).plot(
        ax=axis, color="white", edgecolor="darkslategrey", linewidth=0.5
    )
    axis.set_title(data_xrm["season"][i].values)

plt.show()

fig = plt.figure(layout="constrained", figsize=(10, 4))
subfigs = fig.subfigures(2, 1)

var = "gro"
plot_transform = cplt.rotated_pole_transform(data_xrm)
cmap = cplt.colormap_configs(var)

subfigs[0] = data_xrm[var].plot.contourf(
    x="rlon",
    y="rlat",
    col="season",
    # col_wrap=columns_cbar_aspect[0],
    cmap=cmap,
    robust=True,
    cbar_kwargs={
        # "aspect": columns_cbar_aspect[1],
        "label": (
            f"{data_xrm[var].attrs['long_name']}\n"
            f"[{data_xrm[var].attrs['units']}]"
        )
    },
    transform=plot_transform,
    subplot_kws={"projection": cplt.plot_projection},
    # levels=cbar_levels,
    xlim=(-1.9, 1.6),
    ylim=(-2.1, 2.1),
    aspect=0.9,
)

subfigs[1] = data_xrm[var].plot.contourf(
    x="rlon",
    y="rlat",
    col="season",
    # col_wrap=columns_cbar_aspect[0],
    cmap=cmap,
    robust=True,
    cbar_kwargs={
        # "aspect": columns_cbar_aspect[1],
        "label": (
            f"{data_xrm[var].attrs['long_name']}\n"
            f"[{data_xrm[var].attrs['units']}]"
        )
    },
    transform=plot_transform,
    subplot_kws={"projection": cplt.plot_projection},
    # levels=cbar_levels,
    xlim=(-1.9, 1.6),
    ylim=(-2.1, 2.1),
    aspect=0.9,
)

plt.show()

import matplotlib.pyplot as plt
import numpy as np


def example_plot(ax, fontsize=12, hide_labels=False):
    pc = ax.pcolormesh(np.random.randn(30, 30), vmin=-2.5, vmax=2.5)
    if not hide_labels:
        ax.set_xlabel("x-label", fontsize=fontsize)
        ax.set_ylabel("y-label", fontsize=fontsize)
        ax.set_title("Title", fontsize=fontsize)
    return pc


np.random.seed(19680808)
# gridspec inside gridspec
fig = plt.figure(layout="constrained", figsize=(10, 4))
subfigs = fig.subfigures(1, 2, wspace=0.07)

axsLeft = subfigs[0].subplots(1, 2, sharey=True)
subfigs[0].set_facecolor("0.75")
for ax in axsLeft:
    pc = example_plot(ax)
subfigs[0].suptitle("Left plots", fontsize="x-large")
subfigs[0].colorbar(pc, shrink=0.6, ax=axsLeft, location="bottom")

axsRight = subfigs[1].subplots(3, 1, sharex=True)
for nn, ax in enumerate(axsRight):
    pc = example_plot(ax, hide_labels=True)
    if nn == 2:
        ax.set_xlabel("xlabel")
    if nn == 1:
        ax.set_ylabel("ylabel")

subfigs[1].set_facecolor("0.85")
subfigs[1].colorbar(pc, shrink=0.6, ax=axsRight)
subfigs[1].suptitle("Right plots", fontsize="x-large")

fig.suptitle("Figure suptitle", fontsize="xx-large")

plt.show()

# ### Unweighted

data_xru = data_xr.groupby("time.season").mean()
data_xru = data_xru.reindex(season=["DJF", "MAM", "JJA", "SON"])

data_xru

var = "gro"
plot_transform = cplt.rotated_pole_transform(data_xru)
cmap = cplt.colormap_configs(var)

fig = data_xru[var].plot.contourf(
    x="rlon",
    y="rlat",
    col="season",
    # col_wrap=columns_cbar_aspect[0],
    cmap=cmap,
    robust=True,
    cbar_kwargs={
        # "aspect": columns_cbar_aspect[1],
        "label": (
            f"{data_xru[var].attrs['long_name']}\n"
            f"[{data_xru[var].attrs['units']}]"
        )
    },
    transform=plot_transform,
    subplot_kws={"projection": cplt.plot_projection},
    # levels=cbar_levels,
    xlim=(-1.9, 1.6),
    ylim=(-2.1, 2.1),
    aspect=0.9,
)

for i, axis in enumerate(fig.axs.flat):
    ie_bbox.to_crs(cplt.plot_projection).plot(
        ax=axis, color="white", edgecolor="darkslategrey", linewidth=0.5
    )
    axis.set_title(data_xru["season"][i].values)

plt.show()

datasets = {}

for exp, model, data in itertools.product(
    ["historical", "rcp45", "rcp85"],
    ["CNRM-CM5", "EC-EARTH", "HadGEM2-ES", "MPI-ESM-LR"],
    ["EURO-CORDEX"]
    # ["EURO-CORDEX", "HiResIreland"]
):
    # auto-rechunking may cause NotImplementedError with object dtype
    # where it will not be able to estimate the size in bytes of object data
    if model == "HadGEM2-ES":
        CHUNKS = 300
    else:
        CHUNKS = "auto"

    datasets[f"{data}_{model}_{exp}"] = xr.open_mfdataset(
        glob.glob(
            os.path.join(
                "data",
                "ModVege",
                data,
                exp,
                model,
                f"*{data}*{model}*{exp}*.nc",
            )
        ),
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

list(datasets.keys())

datasets["EURO-CORDEX_EC-EARTH_rcp45"]

varlist = ["bm", "pgro", "gro", "i_bm", "c_bm", "h_bm"]

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

for var in ["bm", "pgro", "gro"]:
    data_pivot = pd.pivot_table(
        data_all[var], values=var, columns="legend", index=data_all[var].index
    )
    data_pivot.plot(
        kind="hist",
        subplots=True,
        figsize=(12, 15),
        bins=50,
        sharex=True,
        sharey=True,
        layout=(6, 4),
        title=(
            datasets["EURO-CORDEX_EC-EARTH_rcp45"][var].attrs["long_name"]
            + f" [{datasets['EURO-CORDEX_EC-EARTH_rcp45'][var].attrs['units']}]"
            f" at Moorepark ({LON}, {LAT})"
        ),
    )
    plt.tight_layout()
    plt.show()

# ## Seasonal maps

# ### Mean

# #### Weighted vs. unweighted mean

cfacet.plot_season_diff(
    data=datasets["EURO-CORDEX_EC-EARTH_rcp45"],
    var="gro",
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
    datasets["EURO-CORDEX_EC-EARTH_rcp45"],
    var="gro",
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
