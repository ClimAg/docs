# %% [markdown]
# # CORINE land cover 2018 data
#
# <https://land.copernicus.eu/pan-european/corine-land-cover/clc2018>

# %%
# import libraries
import multiprocessing
import os
import platform
from datetime import datetime, timezone
from zipfile import BadZipFile, ZipFile

# Windows
if platform.system() == "Windows":
    import multiprocessing.popen_spawn_win32
# Linux/OSX
else:
    import multiprocessing.popen_spawn_posix

import threading
import xml.etree.ElementTree as ET

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import rioxarray as rxr
from dask.distributed import Client, LocalCluster, Lock
from dask.utils import SerializableLock
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

import climag.plot_configs

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
# define data directories
DATA_DIR_BASE = os.path.join("data", "land-cover", "clc-2018")

# %%
# the ZIP file containing the CLC 2018 data should be moved to this folder
DATA_DIR = os.path.join(DATA_DIR_BASE, "raw")

# %%
os.listdir(DATA_DIR)

# %%
ZIP_FILE = os.path.join(
    DATA_DIR, "83684d24c50f069b613e0dc8e12529b893dc172f.zip"
)

# %%
# list of files/folders in the ZIP archive
ZipFile(ZIP_FILE).namelist()

# %%
# extract the archive
try:
    z = ZipFile(ZIP_FILE)
    z.extractall(DATA_DIR)
except BadZipFile:
    print("There were issues with the file", ZIP_FILE)

# %%
ZIP_FILE = os.path.join(
    DATA_DIR, "u2018_clc2018_v2020_20u1_raster100m.zip"
)

# %%
# list of TIF files in the new ZIP archive
for i in ZipFile(ZIP_FILE).namelist():
    if i.endswith(".tif"):
        print(i)

# %%
# extract the ZIP file
try:
    z = ZipFile(ZIP_FILE)
    z.extractall(DATA_DIR)
except BadZipFile:
    print("There were issues with the file", ZIP_FILE)

# %%
DATA_DIR = os.path.join(
    DATA_DIR_BASE, "raw", "u2018_clc2018_v2020_20u1_raster100m", "DATA"
)

# %%
FILE_PATH = os.path.join(DATA_DIR, "U2018_CLC2018_V2020_20u1.tif")

# %%
# read the CLC 2018 raster
# use Dask for parallel computing
# https://corteva.github.io/rioxarray/stable/examples/dask_read_write.html
with LocalCluster() as cluster, Client(cluster) as client:
    landcover = rxr.open_rasterio(
        FILE_PATH,
        chunks=True,
        cache=False,
        lock=False,
        # lock=Lock("rio-read", client=client)  # when too many file handles open
    )
    landcover.rio.to_raster(
        os.path.join(DATA_DIR_BASE, "dask_multiworker.tif"),
        tiled=True,
        lock=Lock("rio", client=client)
    )

# %%
landcover

# %%
landcover.rio.resolution()

# %%
landcover.rio.bounds()

# %%
landcover.rio.crs

# %%
# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="Boundary_IE_NUTS")

# %%
# convert the boundary's CRS to match the CLC raster's CRS
ie.to_crs(landcover.rio.crs, inplace=True)

# %%
ie

# %%
# clip land cover to Ireland's boundary
landcover = rxr.open_rasterio(
    FILE_PATH, cache=False, masked=True
).rio.clip(ie["geometry"], from_disk=True)

# %%
landcover

# %%
landcover.rio.bounds()

# %%
# export to GeoTIFF
landcover.rio.to_raster(
    os.path.join(DATA_DIR_BASE, "clc-2018-ie.tif"), windowed=True, tiled=True
)

# %%
# get unique value count for the raster
uniquevals = gpd.GeoDataFrame(
    np.unique(landcover, return_counts=True)
).transpose()
# assign column names
uniquevals.columns = ["value", "count"]

# %%
# drop row(s) with NaN
uniquevals.dropna(inplace=True)
# sort by count
uniquevals = uniquevals.sort_values("count", ascending=False)
# convert value column to string
uniquevals["value"] = uniquevals["value"].astype(int).astype(str)

# %%
uniquevals

# %%
# read the QGIS style file containing the legend entries
tree = ET.parse(os.path.join(
    DATA_DIR_BASE,
    "raw",
    "u2018_clc2018_v2020_20u1_raster100m",
    "Legend",
    "clc_legend_qgis_raster.qml"
))
root = tree.getroot()

# %%
# extract colour palette
pal = {}

for palette in root.iter("paletteEntry"):
    pal[palette.attrib["value"]] = palette.attrib

# %%
# generate data frame from palette dictionary
legend = gpd.GeoDataFrame.from_dict(pal).transpose()
legend = gpd.GeoDataFrame(legend)

# %%
# convert value column to string
legend["value"] = legend["value"].astype(str)
legend.drop(columns="alpha", inplace=True)

# %%
legend

# %%
# merge unique value dataframe with legend
uniquevals = uniquevals.merge(legend, on="value")
uniquevals = uniquevals.sort_values("count", ascending=False)

# %%
# calculate percentage based on count
uniquevals["percentage"] = (
    uniquevals["count"] / uniquevals["count"].sum() * 100
)
uniquevals["percentage"] = uniquevals["percentage"].round(1)

# %%
uniquevals

# %%
# plot major land cover types, i.e. percentage > 1
mask = uniquevals["percentage"] > 1
uniquevals_sig = uniquevals[mask]

ax = uniquevals_sig.plot.barh(
    x="label", y="percentage", legend=False, figsize=(9, 6),
    color=uniquevals_sig["color"]
)
ax.bar_label(ax.containers[0], padding=3)
plt.title("Major land cover types for Ireland based on CLC 2018 data")
plt.ylabel("")
plt.xlabel("%")
plt.show()

# %%
# convert values to integer and sort
uniquevals["value"] = uniquevals["value"].astype(int)
uniquevals.sort_values("value", inplace=True)

# %%
# create a colourmap for the plot
colours = list(uniquevals["color"])
nodes = np.array(uniquevals["value"])
# normalisation
nodes = (nodes - min(nodes)) / (max(nodes) - min(nodes))
colours = LinearSegmentedColormap.from_list(
    "CLC2018", list(zip(nodes, colours))
)
colours

# %%
col_discrete = ListedColormap(list(uniquevals["color"]))
col_discrete

# %%
img = plt.figure(figsize=(15, 15))
img = plt.imshow(np.array([[0, len(uniquevals)]]), cmap=col_discrete)
img.set_visible(False)

ticks = list(np.arange(.5, len(uniquevals) + .5, 1))
cbar = plt.colorbar(ticks=ticks)
cbar.ax.set_yticklabels(list(uniquevals["label"]))

landcover.plot(add_colorbar=False, cmap=colours)

plt.title("CLC 2018 - Ireland [EPSG:3035]")

plt.axis("equal")
plt.xlim(landcover.rio.bounds()[0] - 9e3, landcover.rio.bounds()[1] + 9e3)
plt.ylim(landcover.rio.bounds()[2] - 9e3, landcover.rio.bounds()[3] + 9e3)

plt.show()

# %%
# reproject to Irish transverse mercator
landcover = landcover.rio.reproject("EPSG:2157")

# %%
img = plt.figure(figsize=(15, 15))
img = plt.imshow(np.array([[0, len(uniquevals)]]), cmap=col_discrete)
img.set_visible(False)

ticks = list(np.arange(.5, len(uniquevals) + .5, 1))
cbar = plt.colorbar(ticks=ticks)
cbar.ax.set_yticklabels(list(uniquevals["label"]))

landcover.plot(add_colorbar=False, cmap=colours)

plt.title("CLC 2018 - Ireland [EPSG:2157]")
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")

plt.axis("equal")
plt.xlim(landcover.rio.bounds()[0], landcover.rio.bounds()[2])
plt.ylim(landcover.rio.bounds()[1], landcover.rio.bounds()[3])

plt.show()

# %% [markdown]
# ## QGIS
#
# Unique value counts can also be generated using QGIS.
#
# Run the following code snippets in the QGIS Python console.

# %%
# generate statistics for the unique values

# params = {
#     "INPUT": os.path.join(DATA_DIR_BASE, "clc-2018-ie.tif"),
#     "OUTPUT_HTML_FILE": os.path.join(DATA_DIR_BASE, "raster_unique_vals.html"),
#     "OUTPUT_TABLE": os.path.join(DATA_DIR_BASE, "raster_unique_vals.geojson")
# }

# processing.run("native:rasterlayeruniquevaluesreport", params)

# %%
# apply the raster's style file to view the legend

# params = {
#     "INPUT": os.path.join(DATA_DIR_BASE, "clc-2018-ie.tif"),
#     "STYLE": os.path.join(
#         DATA_DIR,
#         "u2018_clc2018_v2020_20u1_raster100m",
#         "Legend",
#         "clc_legend_qgis_raster.qml"
#     )
# }

# processing.run("native:setlayerstyle", params)
