#!/usr/bin/env python
# coding: utf-8

# # Visualising climate model datasets

# import libraries
import os
import glob
import itertools
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import xarray as xr
from dask.distributed import Client
import climag.plot_configs as cplt

print("Last updated:", datetime.now(tz=timezone.utc))

client = Client(n_workers=2, threads_per_worker=4, memory_limit="3GB")

client

DATA_DIR_BASE = os.path.join("data", "EURO-CORDEX", "IE")

# Moorepark met station coords
LON, LAT = -8.26389, 52.16389
# # Valentia Observatory met station coords
# LON_V, LAT_V = -10.24333, 51.93806

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")
ie_bbox = gpd.read_file(
    GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE_BBOX_DIFF"
)

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
        glob.glob(os.path.join("data", data, "IE", f"*{model}*{exp}*.nc"))[0],
        chunks=CHUNKS,
        decode_coords="all",
    )

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

for var in varlist:
    data_pivot = pd.pivot_table(
        data_all[var], values=var, columns="dataset", index=data_all[var].index
    )
    data_pivot.plot(
        kind="hist",
        subplots=True,
        figsize=(12, 6),
        bins=50,
        sharex=True,
        sharey=True,
        layout=(2, 4),
        title=(
            datasets["EURO-CORDEX_EC-EARTH_rcp45"][var].attrs["long_name"]
            + f" [{datasets['EURO-CORDEX_EC-EARTH_rcp45'][var].attrs['units']}]"
            f" at Moorepark ({LON}, {LAT})"
        ),
    )
    plt.tight_layout()
    plt.show()

# ## Averages

# ### Annual averages

# ### Monthly averages

# ### Seasonal averages

for var in data.data_vars:
    cplt.plot_averages(
        data=data.sel(time=slice("1976", "2005")),
        var=var,
        averages="season",
        boundary_data=ie_bbox,
        cbar_levels=12,
    )

# ### Time series

data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

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

data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest").sel(
    time=slice("1976", "2005")
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
