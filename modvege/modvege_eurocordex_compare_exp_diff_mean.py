#!/usr/bin/env python
# coding: utf-8

# # ModVege results - EURO-CORDEX - Difference in mean b/w hist/rcp

# import libraries
import glob
import os
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import climag.plot_configs as cplt

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries.gpkg")
ie_bbox = gpd.read_file(GPKG_BOUNDARY, layer="ne_10m_land_2157_IE_BBOX_DIFF")

data = {}
stat = "mean"

data[stat] = xr.open_mfdataset(
    glob.glob(
        os.path.join(
            "data", "ModVege", "stats", f"*EURO-CORDEX*{stat}_season.nc"
        )
    ),
    decode_coords="all",
    chunks="auto",
)
data[f"{stat}_diff"] = xr.combine_by_coords(
    [
        (data[stat].sel(exp="rcp45") - data[stat].sel(exp="historical"))
        .assign_coords(exp="rcp45 - historical")
        .expand_dims(dim="exp"),
        (data[stat].sel(exp="rcp85") - data[stat].sel(exp="historical"))
        .assign_coords(exp="rcp85 - historical")
        .expand_dims(dim="exp"),
    ]
)
for var in data[f"{stat}_diff"].data_vars:
    data[f"{stat}_diff"][var].attrs = data[stat][var].attrs
data[f"{stat}_diff"].rio.write_crs(data[stat].rio.crs)

# cumulative vars
data[f"{stat}_c"] = xr.open_mfdataset(
    glob.glob(
        os.path.join(
            "data", "ModVege", "stats", f"*EURO-CORDEX*{stat}_cumulative.nc"
        )
    ),
    decode_coords="all",
    chunks="auto",
)
data[f"{stat}_c_diff"] = xr.combine_by_coords(
    [
        (
            data[f"{stat}_c"].sel(exp="rcp45")
            - data[f"{stat}_c"].sel(exp="historical")
        )
        .assign_coords(exp="rcp45 - historical")
        .expand_dims(dim="exp"),
        (
            data[f"{stat}_c"].sel(exp="rcp85")
            - data[f"{stat}_c"].sel(exp="historical")
        )
        .assign_coords(exp="rcp85 - historical")
        .expand_dims(dim="exp"),
    ]
)
for var in data[f"{stat}_c_diff"].data_vars:
    data[f"{stat}_c_diff"][var].attrs = data[f"{stat}_c"][var].attrs
data[f"{stat}_c_diff"].rio.write_crs(data[f"{stat}_c"].rio.crs)

data["mean"]

data["mean_c"]

notnull = xr.open_dataset(
    os.path.join(
        "data",
        "ModVege",
        "EURO-CORDEX",
        "historical",
        "CNRM-CM5",
        "modvege_IE_EURO-CORDEX_RCA4_CNRM-CM5_historical_1976.nc",
    ),
    decode_coords="all",
    chunks="auto",
)
notnull = pd.notnull(notnull["gro"].isel(time=0))


def plot_all(data, var, season, levels=None, ticks=None):
    """
    Helper function to plot facet maps
    """

    plot_transform = cplt.rotated_pole_transform(data)

    cbar_kwargs = {
        "label": (
            f"{data[var].attrs['long_name']} [{data[var].attrs['units']}]"
        )
    }

    if ticks is not None:
        cbar_kwargs["ticks"] = ticks

    if len(data["exp"]) == 3:
        cmap = cplt.colormap_configs(var)
        cbar_kwargs["aspect"] = 30
        figsize = (12.45, 9.25)
        extend = "max"
        robust = False
    else:
        cmap = "RdBu"
        cbar_kwargs["aspect"] = 19
        figsize = (12.35, 6.25)
        extend = "both"
        robust = True

    if season is not None:
        data = data.sel(season=season)
    fig = (
        data[var]
        .where(notnull)
        .plot.contourf(
            x="rlon",
            y="rlat",
            col="model",
            row="exp",
            cmap=cmap,
            extend=extend,
            robust=robust,
            cbar_kwargs=cbar_kwargs,
            transform=plot_transform,
            subplot_kws={"projection": cplt.plot_projection},
            levels=levels,
            xlim=(-1.775, 1.6),
            ylim=(-2.1, 2.1),
            figsize=figsize,
        )
    )

    # if season is not None:
    #     plt.suptitle(season, size=16, y=1.0275, x=0.4125)

    fig.set_titles("{value}", weight="semibold", fontsize=14)

    # add boundary
    for axis in fig.axs.flat:
        try:
            ie_bbox.to_crs(cplt.plot_projection).plot(
                ax=axis,
                edgecolor="darkslategrey",
                color="white",
                linewidth=0.5,
            )
        except NameError:
            axis.coastlines(
                resolution="10m", color="darkslategrey", linewidth=0.5
            )

    plt.show()


season_list = ["DJF", "MAM", "JJA", "SON"]

# ## Total growth (daily)

for season in season_list:
    plot_all(
        data=data["mean_diff"],
        var="gro",
        season=season,
        levels=[-24 + 1.92 * n for n in range(26)],
        ticks=[-24 + 8 * n for n in range(7)],
    )

# ## Potential growth (daily)

for season in season_list:
    plot_all(
        data=data["mean_diff"],
        var="pgro",
        season=season,
        levels=[-30 + 2.4 * n for n in range(26)],
        ticks=[-30 + 10 * n for n in range(7)],
    )

# ## Total ingestion (daily)

for season in season_list:
    plot_all(
        data=data["mean_diff"],
        var="c_bm",
        season=season,
        levels=[-7.5 + 0.6 * n for n in range(26)],
        ticks=[-7.5 + 2.5 * n for n in range(7)],
    )

# ## Standing biomass (cumulative)

for season in season_list:
    plot_all(
        data=data["mean_diff"],
        var="bm",
        season=season,
        levels=[-900 + 72 * n for n in range(26)],
        ticks=[-900 + 300 * n for n in range(7)],
    )

# ## Senescence (daily)

for season in season_list:
    plot_all(
        data=data["mean_diff"],
        var="sen",
        season=season,
        levels=[-15 + 1.2 * n for n in range(26)],
        ticks=[-15 + 5 * n for n in range(7)],
    )

# ## Abscission (daily)

for season in season_list:
    plot_all(
        data=data["mean_diff"],
        var="abs",
        season=season,
        levels=[-15 + 1.2 * n for n in range(26)],
        ticks=[-15 + 5 * n for n in range(7)],
    )

# ## Ingested biomass (yearly total)

plot_all(
    data=data["mean_c_diff"],
    var="i_bm",
    season=None,
    levels=[-750 + 60 * n for n in range(26)],
    ticks=[-750 + 250 * n for n in range(7)],
)

# ## Harvested biomass (yearly total)

plot_all(
    data=data["mean_c_diff"],
    var="h_bm",
    season=None,
    levels=[-450 + 36 * n for n in range(26)],
    ticks=[-450 + 150 * n for n in range(7)],
)

print("Last updated:", datetime.now(tz=timezone.utc))
