#!/usr/bin/env python
# coding: utf-8

# # ModVege results - EURO-CORDEX - Difference in mean b/w hist/obs

# import libraries
import glob
import os
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import climag.plot_configs as cplt
import rasterio as rio

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries.gpkg")
ie_bbox = gpd.read_file(GPKG_BOUNDARY, layer="ne_10m_land_2157_IE_BBOX_DIFF")

data = {}
stat = "mean"

data["EURO-CORDEX"] = xr.open_mfdataset(
    glob.glob(
        os.path.join(
            "data", "ModVege", "stats", f"*EURO-CORDEX*{stat}_season_MERA.nc"
        )
    ),
    decode_coords="all",
    chunks="auto",
)

data["EURO-CORDEX"] = data["EURO-CORDEX"].isel(exp=0)

data["MERA"] = xr.open_mfdataset(
    glob.glob(
        os.path.join("data", "ModVege", "stats", f"*MERA*{stat}_season.nc")
    ),
    decode_coords="all",
    chunks="auto",
)

# reassign projection
data["MERA"].rio.write_crs(cplt.lambert_conformal, inplace=True)

data["EURO-CORDEX_c"] = xr.open_mfdataset(
    glob.glob(
        os.path.join(
            "data",
            "ModVege",
            "stats",
            f"*EURO-CORDEX*{stat}_cumulative_MERA.nc",
        )
    ),
    decode_coords="all",
    chunks="auto",
)

data["EURO-CORDEX_c"] = data["EURO-CORDEX_c"].isel(exp=0)

data["MERA_c"] = xr.open_mfdataset(
    glob.glob(
        os.path.join("data", "ModVege", "stats", f"*MERA*{stat}_cumulative.nc")
    ),
    decode_coords="all",
    chunks="auto",
)

# reassign projection
data["MERA_c"].rio.write_crs(cplt.lambert_conformal, inplace=True)

data["EURO-CORDEX"]

season_list = ["DJF", "MAM", "JJA", "SON"]

# regrid climate model data
for season in season_list:
    data[season] = data["EURO-CORDEX"].drop(["lat", "lon", "exp"])
    data[season] = data[season].rename({"rlon": "x", "rlat": "y"})
    data[season] = data[season].sel(season=season)
    data[season] = data[season].rio.reproject_match(
        data["MERA"], resampling=rio.enums.Resampling.bilinear
    )
    data[season] = data[season].assign_coords(
        {"x": data["MERA"]["x"], "y": data["MERA"]["y"]}
    )

data["EURO-CORDEX"] = xr.combine_by_coords(
    [
        data["DJF"].expand_dims(dim="season"),
        data["MAM"].expand_dims(dim="season"),
        data["JJA"].expand_dims(dim="season"),
        data["SON"].expand_dims(dim="season"),
    ]
)

data["EURO-CORDEX"]

data["diff"] = data["EURO-CORDEX"] - data["MERA"]

for var in data["diff"].data_vars:
    data["diff"][var].attrs = data["MERA"][var].attrs

# sort seasons in the correct order
data["diff"] = data["diff"].reindex(season=season_list)

# data[f"{stat}_diff"] = xr.combine_by_coords([
#     (
#         data[stat].sel(exp="rcp45") - data[stat].sel(exp="historical")
#     ).assign_coords(exp="rcp45 - historical").expand_dims(dim="exp"),
#     (
#         data[stat].sel(exp="rcp85") - data[stat].sel(exp="historical")
#     ).assign_coords(exp="rcp85 - historical").expand_dims(dim="exp")
# ])
# for var in data[f"{stat}_diff"].data_vars:
#     data[f"{stat}_diff"][var].attrs = data[stat][var].attrs
# data[f"{stat}_diff"].rio.write_crs(data[stat].rio.crs)

# for stat in stat_list:
#     data[f"{stat}_c"] = xr.open_mfdataset(
#         glob.glob(
#             os.path.join(
#                 "data", "ModVege", "stats",
#                 f"*EURO-CORDEX*{stat}_cumulative.nc"
#             )
#         ),
#         decode_coords="all", chunks="auto"
#     )
#     data[f"{stat}_c_diff"] = xr.combine_by_coords([
#         (
#             data[f"{stat}_c"].sel(exp="rcp45") -
#             data[f"{stat}_c"].sel(exp="historical")
#         ).assign_coords(exp="rcp45 - historical").expand_dims(dim="exp"),
#         (
#             data[f"{stat}_c"].sel(exp="rcp85") -
#             data[f"{stat}_c"].sel(exp="historical")
#         ).assign_coords(exp="rcp85 - historical").expand_dims(dim="exp")
#     ])
#     for var in data[f"{stat}_c_diff"].data_vars:
#         data[f"{stat}_c_diff"][var].attrs = data[f"{stat}_c"][var].attrs
#     data[f"{stat}_c_diff"].rio.write_crs(data[f"{stat}_c"].rio.crs)


def plot_all(data, var, levels=None, ticks=None):
    """
    Helper function to plot facet maps
    """

    plot_transform = cplt.lambert_conformal

    cbar_kwargs = {
        "label": (
            f"{data[var].attrs['long_name']} [{data[var].attrs['units']}]"
        )
    }

    if ticks is not None:
        cbar_kwargs["ticks"] = ticks

    cmap = "RdBu"
    cbar_kwargs["aspect"] = 37.5
    figsize = (12.5, 12.5)
    extend = "both"
    robust = True

    fig = data[var].plot.contourf(
        x="x",
        y="y",
        row="season",
        col="model",
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

plot_all(
    data=data["diff"],
    var="gro",
    levels=[-60 + 4.8 * n for n in range(26)],
    ticks=[-60 + 20 * n for n in range(7)],
)

# ## Potential growth (daily)

plot_all(
    data=data["diff"],
    var="pgro",
    levels=[-120 + 9.6 * n for n in range(26)],
    ticks=[-120 + 40 * n for n in range(7)],
)

# ## Total ingestion (daily)

plot_all(
    data=data["diff"],
    var="c_bm",
    levels=[-15 + 1.2 * n for n in range(26)],
    ticks=[-15 + 5 * n for n in range(7)],
)

# ## Standing biomass (cumulative)

plot_all(
    data=data["diff"],
    var="bm",
    levels=[-2400 + 192 * n for n in range(26)],
    ticks=[-2400 + 800 * n for n in range(7)],
)

# ## Senescence (daily)

plot_all(
    data=data["diff"],
    var="sen",
    levels=[-60 + 4.8 * n for n in range(26)],
    ticks=[-60 + 20 * n for n in range(7)],
)

# ## Abscission (daily)

plot_all(
    data=data["diff"],
    var="abs",
    levels=[-30 + 2.4 * n for n in range(26)],
    ticks=[-30 + 10 * n for n in range(7)],
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
