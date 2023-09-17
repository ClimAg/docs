#!/usr/bin/env python
# coding: utf-8

# # Agro-environmental regions in Ireland
#
# Agro-environmental regions described in Holden and Brereton (2004) derived
# from February rainfall data
#
# A screenshot of the map in the paper was taken and georeferenced into vector
# data
#
# Holden, N. M. and Brereton, A. J. (2004). 'Definition of agroclimatic regions
# in Ireland using hydro-thermal and crop yield data', Agricultural and Forest
# Meteorology, vol. 122, no. 3, pp. 175-191. DOI:
# [10.1016/j.agrformet.2003.09.010][DOI].
#
# [DOI]: https://doi.org/10.1016/j.agrformet.2003.09.010

# import libraries
import os
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import ticker
import climag.plot_configs as cplt

print("Last updated:", datetime.now(tz=timezone.utc))

# define data path
DATA_DIR = os.path.join(
    "data",
    "climatic-regions",
    "agro-environmental-regions",
    "agro-environmental-regions.gpkg",
)

data = gpd.read_file(DATA_DIR, layer="agro-environmental-regions")

data

data.crs

data.shape

ax = data.plot(
    column="Cluster",
    legend=True,
    figsize=(9, 9),
    cmap="Set3",
    legend_kwds=dict(loc="upper left"),
)

# ax.xaxis.set_major_formatter(cplt.longitude_tick_format)
# ax.yaxis.set_major_formatter(cplt.latitude_tick_format)
# ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

for legend_handle in ax.get_legend().legendHandles:
    legend_handle.set_markeredgewidth(0.2)
    legend_handle.set_markeredgecolor("darkslategrey")
ax.axes.tick_params(labelbottom=False, labelleft=False)

data.boundary.plot(ax=ax, color="darkslategrey", linewidth=0.5)

plt.text(-7, 51.3, "Holden and Brereton (2004)")
plt.title("Agro-environmental regions in Ireland")
plt.show()
