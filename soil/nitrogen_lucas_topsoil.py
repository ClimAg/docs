# %% [markdown]
# # Nitrogen nutritional index
#
# Soil chemical properties based on LUCAS topsoil data (Ballabio et al., 2019; European Commission, n.d.; Panagos et al., 2022; Panagos et al., 2012): https://esdac.jrc.ec.europa.eu/content/chemical-properties-european-scale-based-lucas-topsoil-data

# %%
import geopandas as gpd
import matplotlib.pyplot as plt
from zipfile import BadZipFile, ZipFile
import rioxarray as rxr
from rasterstats import zonal_stats

# %%
DATA_DIR = os.path.join("data", "soil", "chemical-properties-european-scale-based-lucas-topsoil-data")

# %%
ZIP_FILE = os.path.join(DATA_DIR, "N.zip")

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
DATA_FILE = os.path.join(DATA_DIR, "N.tif")

# %%
data = rxr.open_rasterio(DATA_FILE, chunks="auto", masked=True)

# %%
data

# %%
data.rio.crs

# %%
data.rio.resolution()

# %%
# Ireland boundary
GPKG_BOUNDARY = os.path.join(
    "data", "boundaries", "NUTS2021", "NUTS_2021.gpkg"
)
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")

# %%
ie.crs

# %%
# clip raster to Ireland's boundary
data = rxr.open_rasterio(
    DATA_FILE, chunks="auto", masked=True
).rio.clip(ie.to_crs(data.rio.crs)["geometry"])

# %%
data

# %%
data.max().values

# %%
data.min().values

# %%
fig = data.plot(
    robust=True, cmap="viridis_r", figsize=(7, 7),
    cbar_kwargs=dict(label="Topsoil nitrogen content [g kg⁻¹]")
)
ie.to_crs(data.rio.crs).boundary.plot(ax=fig.axes, color="darkslategrey", linewidth=1)
plt.title(None)
fig.axes.tick_params(labelbottom=False, labelleft=False)
plt.xlabel("")
plt.ylabel("")
plt.tight_layout()
plt.axis("equal")
plt.show()

# %%
# export to GeoTIFF
data.rio.to_raster(os.path.join(DATA_DIR, "IE_N.tif"))

# %% [markdown]
# ## Grid cells

# %%
grid_cells = gpd.read_file(
    os.path.join("data", "ModVege", "params_eurocordex.gpkg"),
    layer="stocking_rate"
)

# %%
grid_cells.head()

# %%
grid_cells.crs

# %%
grid_cells.shape

# %%
fig = data.plot(
    robust=True, cmap="viridis_r", figsize=(7, 7),
    cbar_kwargs=dict(label="Topsoil nitrogen content [g kg⁻¹]")
)
grid_cells.to_crs(data.rio.crs).boundary.plot(ax=fig.axes, color="darkslategrey", linewidth=1)
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
stats = gpd.GeoDataFrame(zonal_stats(vectors=grid_cells.to_crs(data.rio.crs), raster=os.path.join(DATA_DIR, "IE_N.tif"), stats=["count", "mean"]))

# %%
stats.head()

# %%
stats.shape

# %%
stats["mean"].min()

# %%
stats["mean"].max()

# %%
stats["count"].min()

# %%
stats["count"].max()

# %%
stats[stats["count"] == 0]

# %%
grid_cells["mean_topsoil_n"] = stats["mean"]

# %%
grid_cells.head()

# %%
axs = grid_cells.plot(
    column="mean_topsoil_n", cmap="Spectral_r", scheme="equal_interval",
    edgecolor="darkslategrey", linewidth=.2, figsize=(6, 7),
    legend=True, legend_kwds={
        "loc": "upper left", "fmt": "{:.2f}", "title": "Topsoil N [g kg⁻¹]"
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

# %% [markdown]
# ## Normalise

# %%
# normalise between 1.0 and 0.35
grid_cells["ni"] = 0.35 + ((grid_cells["mean_topsoil_n"] - float(grid_cells["mean_topsoil_n"].min())) * (1.0 - 0.35)) / (float(grid_cells["mean_topsoil_n"].max()) - float(grid_cells["mean_topsoil_n"].min()))

# %%
grid_cells.head()

# %%
grid_cells["ni"].max()

# %%
grid_cells["ni"].min()

# %%
axs = grid_cells.plot(
    column="ni", cmap="Spectral_r", scheme="equal_interval",
    edgecolor="darkslategrey", linewidth=.2, figsize=(6, 7),
    legend=True, legend_kwds={
        "loc": "upper left", "fmt": "{:.2f}", "title": "NI"
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
grid_cells["ni"] = grid_cells["ni"].fillna(0.35)

# %%
axs = grid_cells.plot(
    column="ni", cmap="Spectral_r", scheme="equal_interval",
    edgecolor="darkslategrey", linewidth=.2, figsize=(6, 7),
    legend=True, legend_kwds={
        "loc": "upper left", "fmt": "{:.2f}", "title": "NI"
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
grid_cells.drop(columns="mean_topsoil_n", inplace=True)

# %%
grid_cells.to_file(
    os.path.join("data", "ModVege", "params.gpkg"), layer="eurocordex"
)
