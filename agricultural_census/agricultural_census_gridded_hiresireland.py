#!/usr/bin/env python
# coding: utf-8

# # Gridding agricultural census data - HiResIreland
#
# Gridding based on
# <https://james-brennan.github.io/posts/fast_gridding_geopandas/>

import itertools
import os

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import shapely
import xarray as xr

import climag.climag as cplt

# ## Open some gridded climate data

TS_FILE = os.path.join(
    "data", "HiResIreland", "IE", "IE_HiResIreland_COSMO5_EC-EARTH_rcp45.nc"
)

data = xr.open_dataset(TS_FILE, chunks="auto", decode_coords="all")

data

# keep only one variable
data = data.drop_vars(names=["PET", "PP", "PAR"])

data

# copy CRS
crs = data.rio.crs

crs

# ## Use the gridded data's bounds to generate a gridded vector layer

data.rio.bounds()

xmin, ymin, xmax, ymax = data.rio.bounds()
# the difference between two adjacent rotated lat or lon values is the
# cell size
cell_size = float(data["rlat"][1] - data["rlat"][0])

# create the cells in a loop
grid_cells = []
for x0 in np.arange(xmin, xmax + cell_size, cell_size):
    for y0 in np.arange(ymin, ymax + cell_size, cell_size):
        # bounds
        x1 = x0 - cell_size
        y1 = y0 + cell_size
        grid_cells.append(shapely.geometry.box(x0, y0, x1, y1))
grid_cells = gpd.GeoDataFrame(grid_cells, columns=["geometry"], crs=crs)

grid_cells.shape

grid_cells.head()

grid_cells.crs

# ## Subset climate data to visualise the cells

data_ = data.sel(time="2041-06-21")

data_

# find number of grid cells with data
len(data_["T"].values.flatten()[np.isfinite(data_["T"].values.flatten())])

plot_transform = cplt.rotated_pole_transform(data_)
# plt.figure(figsize=(9, 7))
axs = plt.axes(projection=cplt.projection_hiresireland)

# plot data for the variable
data_["T"].plot(
    ax=axs,
    cmap="Spectral_r",
    x="rlon",
    y="rlat",
    robust=True,
    transform=plot_transform,
)
grid_cells.to_crs(cplt.projection_hiresireland).boundary.plot(
    ax=axs, color="darkslategrey", linewidth=0.2
)

axs.set_title(None)
plt.axis("equal")
plt.tight_layout()
plt.show()

# ## Drop grid cells without climate data

grid_centroids = {"wkt": [], "rlon": [], "rlat": []}

for rlon, rlat in itertools.product(
    range(len(data.coords["rlon"])), range(len(data.coords["rlat"]))
):
    data__ = data.isel(rlon=rlon, rlat=rlat)

    # ignore null cells
    if not data__["T"].isnull().all():
        grid_centroids["wkt"].append(
            f"POINT ({float(data__['rlon'].values)} "
            f"{float(data__['rlat'].values)})"
        )
        grid_centroids["rlon"].append(float(data__["rlon"].values))
        grid_centroids["rlat"].append(float(data__["rlat"].values))

grid_centroids = gpd.GeoDataFrame(
    grid_centroids,
    geometry=gpd.GeoSeries.from_wkt(grid_centroids["wkt"], crs=crs),
)

grid_centroids.head()

grid_centroids.shape

grid_centroids.crs

grid_cells = gpd.sjoin(grid_cells, grid_centroids.to_crs(grid_cells.crs))

grid_cells.drop(columns=["wkt", "index_right"], inplace=True)

grid_cells.head()

grid_cells.shape

# plt.figure(figsize=(9, 7))
axs = plt.axes(projection=cplt.projection_hiresireland)

# plot data for the variable
data_["T"].plot(
    ax=axs,
    cmap="Spectral_r",
    x="rlon",
    y="rlat",
    robust=True,
    transform=plot_transform,
)

grid_cells.to_crs(cplt.projection_hiresireland).plot(
    ax=axs, edgecolor="darkslategrey", facecolor="none", linewidth=0.2
)

grid_centroids.to_crs(cplt.projection_hiresireland).plot(
    ax=axs, color="darkslategrey", markersize=0.5
)

axs.set_title(None)
plt.axis("equal")
plt.tight_layout()
plt.show()

# ## Read stocking rate data

stocking_rate = gpd.read_file(
    os.path.join("data", "agricultural_census", "agricultural_census.gpkg"),
    layer="stocking_rate",
)

stocking_rate.crs

stocking_rate.head()

stocking_rate.shape

stocking_rate["stocking_rate"].max()

stocking_rate["stocking_rate"].min()

stocking_rate.plot(column="stocking_rate", cmap="Spectral_r")
plt.tick_params(labelbottom=False, labelleft=False)
plt.show()

# ## Reproject cells to the CRS of the stocking rate data

# use a projected CRS (e.g. 2157) instead of a geographical CRS (e.g. 4326)
grid_cells = grid_cells.to_crs(stocking_rate.crs)

grid_cells.head()

axs = stocking_rate.plot(column="stocking_rate", cmap="Spectral_r")
grid_cells.boundary.plot(color="darkslategrey", linewidth=0.2, ax=axs)
axs.tick_params(labelbottom=False, labelleft=False)
plt.show()

# ## Create gridded stocking rate data

merged = gpd.sjoin(stocking_rate, grid_cells, how="left")

merged.head()

merged.shape

axs = merged.plot(column="stocking_rate", cmap="Spectral_r")
grid_cells.boundary.plot(color="darkslategrey", linewidth=0.2, ax=axs)
axs.tick_params(labelbottom=False, labelleft=False)
plt.show()

# compute stats per grid cell, use the mean stocking rate
dissolve = merged[["stocking_rate", "index_right", "geometry"]].dissolve(
    by="index_right", aggfunc=np.mean
)

dissolve.shape

dissolve.head()

len(dissolve.index.unique())

# merge with cell data
grid_cells.loc[dissolve.index, "sr"] = dissolve["stocking_rate"].values

grid_cells.shape

grid_cells.head()

len(grid_cells["geometry"].unique())

grid_cells["sr"].max()

grid_cells["sr"].min()

plt.figure(figsize=(9, 7))
axs = plt.axes(projection=cplt.projection_hiresireland)

# plot data for the variable
data_["T"].plot(
    ax=axs,
    cmap="Spectral_r",
    x="rlon",
    y="rlat",
    robust=True,
    transform=plot_transform,
)

grid_cells.to_crs(cplt.projection_hiresireland).plot(
    column="sr",
    ax=axs,
    edgecolor="darkslategrey",
    facecolor="none",
    linewidth=0.2,
)

axs.set_title(None)
plt.axis("equal")
plt.tight_layout()
plt.show()

axs = grid_cells.plot(
    column="sr",
    cmap="Spectral_r",
    scheme="equal_interval",
    edgecolor="darkslategrey",
    linewidth=0.2,
    figsize=(6, 7),
    legend=True,
    legend_kwds={
        "loc": "upper left",
        "fmt": "{:.2f}",
        "title": "Stocking rate [LU ha⁻¹]",
    },
    missing_kwds={
        "color": "darkslategrey",
        "edgecolor": "darkslategrey",
        "label": "No data",
    },
)
for legend_handle in axs.get_legend().legend_handles:
    legend_handle.set_markeredgewidth(0.2)
    legend_handle.set_markeredgecolor("darkslategrey")
axs.tick_params(labelbottom=False, labelleft=False)
plt.axis("equal")
plt.tight_layout()
plt.show()

# fill no data with min value
grid_cells["sr"] = grid_cells["sr"].fillna(grid_cells["sr"].min())

axs = grid_cells.plot(
    column="sr",
    cmap="Spectral_r",
    scheme="equal_interval",
    edgecolor="darkslategrey",
    linewidth=0.2,
    figsize=(6, 7),
    legend=True,
    legend_kwds={
        "loc": "upper left",
        "fmt": "{:.2f}",
        "title": "Stocking rate [LU ha⁻¹]",
    },
    missing_kwds={
        "color": "darkslategrey",
        "edgecolor": "darkslategrey",
        "label": "No data",
    },
)
for legend_handle in axs.get_legend().legend_handles:
    legend_handle.set_markeredgewidth(0.2)
    legend_handle.set_markeredgecolor("darkslategrey")
axs.tick_params(labelbottom=False, labelleft=False)
plt.axis("equal")
plt.tight_layout()
plt.show()

grid_cells.to_file(
    os.path.join("data", "ModVege", "params.gpkg"), layer="hiresireland"
)
