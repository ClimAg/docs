#!/usr/bin/env python
# coding: utf-8

# # ModVege results - HiResIreland - Difference in mean - historical and observational (MERA)
#
# - Weighted means take into account the number of days in each month

# import libraries
import glob
import os
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
import rasterio as rio
import xarray as xr
import climag.plot_configs as cplt

# Ireland boundary
ie = gpd.read_file(
    os.path.join("data", "boundaries", "boundaries.gpkg"),
    layer="ne_10m_land_2157_IE",
)
ie_bbox = gpd.read_file(
    os.path.join("data", "boundaries", "boundaries.gpkg"),
    layer="ne_10m_land_2157_IE_BBOX_DIFF",
)

season_list = ["DJF", "MAM", "JJA", "SON"]

data = {}
stat = "mean"
dataset = "HiResIreland"

for x in ["season", "cumulative"]:
    data[f"MERA_{x[0]}"] = xr.open_mfdataset(
        glob.glob(
            os.path.join("data", "ModVege", "stats", f"*MERA*{stat}_{x}.nc")
        ),
        decode_coords="all",
        chunks="auto",
    )

    # reassign projection
    data[f"MERA_{x[0]}"].rio.write_crs(cplt.lambert_conformal, inplace=True)

    data[f"{dataset}_{x[0]}"] = xr.open_mfdataset(
        glob.glob(
            os.path.join(
                "data", "ModVege", "stats", f"*{dataset}*{stat}_{x}_MERA.nc"
            )
        ),
        decode_coords="all",
        chunks="auto",
    )

    data[f"{dataset}_{x[0]}"] = data[f"{dataset}_{x[0]}"].isel(exp=0)

# regrid climate model data
for x in ["season", "cumulative"]:
    data[f"{dataset}_{x[0]}"] = data[f"{dataset}_{x[0]}"].drop(
        ["lat", "lon", "exp"]
    )
    data[f"{dataset}_{x[0]}"] = data[f"{dataset}_{x[0]}"].rename(
        {"rlon": "x", "rlat": "y"}
    )
    if x == "season":
        # split by season first
        for season in season_list:
            data[season] = data[f"{dataset}_{x[0]}"].sel(season=season)
            data[season] = data[season].rio.reproject_match(
                data[f"MERA_{x[0]}"], resampling=rio.enums.Resampling.bilinear
            )
            data[season] = data[season].assign_coords(
                {
                    "x": data[f"MERA_{x[0]}"]["x"],
                    "y": data[f"MERA_{x[0]}"]["y"],
                }
            )

        # combine seasons
        data[f"{dataset}_{x[0]}"] = xr.combine_by_coords(
            [
                data["DJF"].expand_dims(dim="season"),
                data["MAM"].expand_dims(dim="season"),
                data["JJA"].expand_dims(dim="season"),
                data["SON"].expand_dims(dim="season"),
            ]
        )
    else:
        data[f"{dataset}_{x[0]}"] = data[
            f"{dataset}_{x[0]}"
        ].rio.reproject_match(
            data[f"MERA_{x[0]}"], resampling=rio.enums.Resampling.bilinear
        )
        data[f"{dataset}_{x[0]}"] = data[f"{dataset}_{x[0]}"].assign_coords(
            {"x": data[f"MERA_{x[0]}"]["x"], "y": data[f"MERA_{x[0]}"]["y"]}
        )

    # clip to Ireland's boundary
    data[f"{dataset}_{x[0]}"] = data[f"{dataset}_{x[0]}"].rio.clip(
        ie.buffer(1).to_crs(cplt.lambert_conformal), all_touched=True
    )

    # calculate difference
    data[f"MERA_{x[0]}_diff"] = (
        data[f"{dataset}_{x[0]}"] - data[f"MERA_{x[0]}"]
    )

    # reassign attributes
    for var in data[f"MERA_{x[0]}_diff"].data_vars:
        data[f"MERA_{x[0]}_diff"][var].attrs = data[f"MERA_{x[0]}"][var].attrs

    if x == "season":
        # sort seasons in the correct order
        data[f"MERA_{x[0]}_diff"] = data[f"MERA_{x[0]}_diff"].reindex(
            season=season_list
        )


def plot_all(data, var, season, levels=None, ticks=None):
    """
    Helper function to plot facet maps
    """

    plot_transform = cplt.lambert_conformal

    cbar_kwargs = {
        "label": (
            f"{data[var].attrs['long_name']} [{data[var].attrs['units']}]"
        ),
        "aspect": 19,
    }

    if ticks is not None:
        cbar_kwargs["ticks"] = ticks

    if season is not None:
        data = data.sel(season=season)

    fig = data[var].plot.contourf(
        x="x",
        y="y",
        col="model",
        cmap="RdBu",
        extend="both",
        robust=True,
        cbar_kwargs=cbar_kwargs,
        transform=plot_transform,
        subplot_kws={"projection": cplt.plot_projection},
        levels=levels,
        xlim=(-1.775, 1.6),
        ylim=(-2.1, 2.1),
        figsize=(12, 6.25),
    )

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


# ## Total growth (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    plot_all(
        data=data["MERA_s_diff"],
        var="gro",
        season=season,
        levels=[-60 + 4.8 * n for n in range(26)],
        ticks=[-60 + 20 * n for n in range(7)],
    )

# ## Potential growth (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    plot_all(
        data=data["MERA_s_diff"],
        var="pgro",
        season=season,
        levels=[-120 + 9.6 * n for n in range(26)],
        ticks=[-120 + 40 * n for n in range(7)],
    )

# ## Total ingestion (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    plot_all(
        data=data["MERA_s_diff"],
        var="c_bm",
        season=season,
        levels=[-15 + 1.2 * n for n in range(26)],
        ticks=[-15 + 5 * n for n in range(7)],
    )

# ## Standing biomass (cumulative)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    plot_all(
        data=data["MERA_s_diff"],
        var="bm",
        season=season,
        levels=[-2400 + 192 * n for n in range(26)],
        ticks=[-2400 + 800 * n for n in range(7)],
    )

# ## Senescence (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    plot_all(
        data=data["MERA_s_diff"],
        var="sen",
        season=season,
        levels=[-60 + 4.8 * n for n in range(26)],
        ticks=[-60 + 20 * n for n in range(7)],
    )

# ## Abscission (daily)

for season in season_list:
    print("-" * 55 + season + "-" * 55)
    plot_all(
        data=data["MERA_s_diff"],
        var="abs",
        season=season,
        levels=[-30 + 2.4 * n for n in range(26)],
        ticks=[-30 + 10 * n for n in range(7)],
    )

# ## Ingested biomass (yearly total)

plot_all(
    data=data["MERA_c_diff"],
    var="i_bm",
    season=None,
    levels=[-3000 + 240 * n for n in range(26)],
    ticks=[-3000 + 1000 * n for n in range(7)],
)

# ## Harvested biomass (yearly total)

plot_all(
    data=data["MERA_c_diff"],
    var="h_bm",
    season=None,
    levels=[-900 + 72 * n for n in range(26)],
    ticks=[-900 + 300 * n for n in range(7)],
)

print("Last updated:", datetime.now(tz=timezone.utc))
