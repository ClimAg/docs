#!/usr/bin/env python
# coding: utf-8

# # ModVege results - MERA - weighted mean
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
ie_bbox = gpd.read_file(
    os.path.join("data", "boundaries", "boundaries.gpkg"),
    layer="ne_10m_land_2157_IE_BBOX_DIFF",
)

data = {}
stat = "mean"

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


def plot_all(data, var, levels=None, ticks=None):
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

    fig = data[var].plot.contourf(
        x="x",
        y="y",
        col="season",
        cmap="YlGn",
        extend="max",
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

plot_all(data=data["MERA_s"], var="gro", levels=[0 + 9 * n for n in range(11)])

# ## Potential growth (daily)

plot_all(
    data=data["MERA_s"], var="pgro", levels=[0 + 20 * n for n in range(11)]
)

# ## Total ingestion (daily)

plot_all(
    data=data["MERA_s"], var="c_bm", levels=[0 + 3 * n for n in range(11)]
)

# ## Standing biomass (cumulative)

plot_all(
    data=data["MERA_s"], var="bm", levels=[0 + 300 * n for n in range(11)]
)

# ## Senescence (daily)

plot_all(
    data=data["MERA_s"], var="sen", levels=[0 + 7.5 * n for n in range(11)]
)

# ## Abscission (daily)

plot_all(
    data=data["MERA_s"], var="abs", levels=[0 + 3.6 * n for n in range(11)]
)

# ## Ingested biomass (yearly total)

axs = plt.axes(projection=cplt.plot_projection)
data["MERA_c"]["i_bm"].plot.contourf(
    ax=axs,
    cmap="YlGn",
    x="x",
    y="y",
    robust=True,
    transform=cplt.lambert_conformal,
    levels=[0 + 480 * n for n in range(11)],
)
ie_bbox.to_crs(cplt.plot_projection).plot(
    ax=axs, edgecolor="darkslategrey", color="white", linewidth=0.5
)
axs.set_title(None)
plt.axis("equal")
plt.tight_layout()
plt.xlim(-1.5, 1.33)
plt.ylim(-2.05, 2.05)
plt.show()

# ## Harvested biomass (yearly total)

axs = plt.axes(projection=cplt.plot_projection)
data["MERA_c"]["h_bm"].plot.contourf(
    ax=axs,
    cmap="YlGn",
    x="x",
    y="y",
    robust=True,
    transform=cplt.lambert_conformal,
    levels=[0 + 48 * n for n in range(11)],
)
ie_bbox.to_crs(cplt.plot_projection).plot(
    ax=axs, edgecolor="darkslategrey", color="white", linewidth=0.5
)
axs.set_title(None)
plt.axis("equal")
plt.tight_layout()
plt.xlim(-1.5, 1.33)
plt.ylim(-2.05, 2.05)
plt.show()

print("Last updated:", datetime.now(tz=timezone.utc))
