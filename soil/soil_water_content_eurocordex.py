# %% [markdown]
# # Soil water-holding capacity
#
# European soil database derived data - total available water content (TAWC)
# for the topsoil [mm] (European Commission, n.d.; Hiederer, 2013a;
# Hiederer, 2013b):
# https://esdac.jrc.ec.europa.eu/content/european-soil-database-derived-data

# %%
import os
from zipfile import BadZipFile, ZipFile
import matplotlib.pyplot as plt
import geopandas as gpd
import rioxarray as rxr
from rasterstats import zonal_stats

# %%
DATA_DIR = os.path.join(
    "data", "soil", "european-soil-database-derived-data"
)

# %%
ZIP_FILE = os.path.join(DATA_DIR, "STU_EU_Layers.zip")

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
DATA_FILE = os.path.join(DATA_DIR, "STU_EU_T_TAWC.rst")

# %%
data = rxr.open_rasterio(DATA_FILE, chunks="auto", masked=True)

# %%
data

# %%
data.rio.crs

# %%
# ETRS 89 LAEA
data_crs = 3035

# %%
data.rio.write_crs(data_crs, inplace=True)

# %%
data.rio.crs

# %%
data.rio.resolution()

# %%
# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")

# %%
ie.crs

# %%
# clip raster to Ireland's boundary
data = rxr.open_rasterio(
    DATA_FILE, chunks="auto", masked=True
).rio.clip(ie.to_crs(data_crs)["geometry"])

# %%
data

# %%
data.max().values

# %%
data.min().values

# %%
fig = data.plot(
    robust=True, cmap="viridis_r", figsize=(7, 7), levels=10,
    cbar_kwargs={"label": "Total available water content [mm]"}
)
ie.to_crs(data_crs).boundary.plot(
    ax=fig.axes, color="darkslategrey", linewidth=1
)
plt.title(None)
fig.axes.tick_params(labelbottom=False, labelleft=False)
plt.xlabel("")
plt.ylabel("")
plt.tight_layout()
plt.axis("equal")
plt.show()

# %%
# export to GeoTIFF
data.rio.to_raster(os.path.join(DATA_DIR, "IE_TAWC.tif"))

# %% [markdown]
# ## Grid cells

# %%
grid_cells = gpd.read_file(
    os.path.join("data", "ModVege", "params.gpkg"), layer="eurocordex"
)

# %%
grid_cells.head()

# %%
grid_cells.crs

# %%
grid_cells.shape

# %%
fig = data.plot(
    robust=True, cmap="viridis_r", figsize=(7, 7), levels=10,
    cbar_kwargs={"label": "Total available water content [mm]"}
)
grid_cells.to_crs(data_crs).boundary.plot(
    ax=fig.axes, color="darkslategrey", linewidth=1
)
plt.title(None)
fig.axes.tick_params(labelbottom=False, labelleft=False)
plt.xlabel("")
plt.ylabel("")
plt.tight_layout()
plt.axis("equal")
plt.show()

# %% [markdown]
# ## Zonal stats

# %%
grid_cells = gpd.GeoDataFrame.from_features(
    zonal_stats(
        vectors=grid_cells.to_crs(data_crs),
        raster=os.path.join(DATA_DIR, "IE_TAWC.tif"),
        stats=["count", "mean"],
        geojson_out=True,
        nodata=-999999
    ), crs=data_crs
).to_crs(grid_cells.crs)

# %%
grid_cells.head()

# %%
grid_cells.shape

# %%
grid_cells["mean"].min()

# %%
grid_cells["mean"].max()

# %%
grid_cells["count"].min()

# %%
grid_cells["count"].max()

# %%
grid_cells[grid_cells["count"] == 0]

# %%
axs = grid_cells.plot(
    column="mean", cmap="Spectral_r", scheme="equal_interval",
    edgecolor="darkslategrey", linewidth=.2, figsize=(6, 7),
    legend=True, legend_kwds={
        "loc": "upper left", "fmt": "{:.2f}", "title": "TAWC [mm]"
    },
    missing_kwds={
        "color": "darkslategrey", "edgecolor": "darkslategrey",
        "label": "No data"
    }
)
for legend_handle in axs.get_legend().legendHandles:
    legend_handle.set_markeredgewidth(.2)
    legend_handle.set_markeredgecolor("darkslategrey")
axs.tick_params(labelbottom=False, labelleft=False)
plt.axis("equal")
plt.tight_layout()
plt.show()

# %%
grid_cells["whc"] = grid_cells["mean"]

# %%
grid_cells.drop(columns=["mean", "count"], inplace=True)

# %%
grid_cells.head()

# %%
grid_cells.to_file(
    os.path.join("data", "ModVege", "params.gpkg"), layer="eurocordex"
)