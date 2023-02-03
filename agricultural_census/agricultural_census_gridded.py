# %% [markdown]
# # Gridding agricultural census data
#
# <https://james-brennan.github.io/posts/fast_gridding_geopandas/>

# %%
# import libraries
import os
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import shapely
import xarray as xr
import climag.plot_configs as cplt

# %%
TS_FILE = os.path.join(
    "data", "EURO-CORDEX", "IE",
    "IE_EUR-11_ICHEC-EC-EARTH_rcp85_r12i1p1_SMHI-RCA4_v1_day_"
    "20410101-20701231.nc"
)

# %%
data = xr.open_dataset(TS_FILE, chunks="auto", decode_coords="all")

# %%
data

# %%
data = data.drop_vars(names=["PET", "PP", "RG", "PAR"])

# %%
data

# %%
crs = data.rio.crs

# %%
crs

# %%
data.rio.bounds()

# %%
data_ = data.sel(time="2041-06-21T12:00:00.000000000")

# %%
data_

# %%
xmin, ymin, xmax, ymax = data.rio.bounds()
cell_size = float(data["rlat"][1] - data["rlat"][0])
xmin += cell_size
xmax -= cell_size
ymax -= 2 * cell_size

# %%
# create the cells in a loop
grid_cells = []
for x0 in np.arange(xmin, xmax + cell_size, cell_size):
    for y0 in np.arange(ymin, ymax + cell_size, cell_size):
        # bounds
        x1 = x0 - cell_size
        y1 = y0 + cell_size
        grid_cells.append(shapely.geometry.box(x0, y0, x1, y1))
cell = gpd.GeoDataFrame(grid_cells, columns=["geometry"], crs=crs)

# %%
plot_transform = cplt.rotated_pole_transform(data)
plt.figure(figsize=(9, 7))
axs = plt.axes(projection=cplt.plot_projection)

# plot data for the variable
data_["T"].plot(
    ax=axs,
    cmap="Spectral_r",
    x="rlon",
    y="rlat",
    robust=True,
    transform=plot_transform
)
cell.to_crs(cplt.plot_projection).boundary.plot(
    ax=axs, color="darkslategrey", linewidth=.2
)

axs.set_title(None)
plt.axis("equal")
plt.tight_layout()
plt.show()

# %%
sr = gpd.read_file(
    os.path.join("data", "agricultural_census", "agricultural_census.gpkg"),
    layer="stocking_rate"
)

# %%
sr.crs

# %%
sr.head()

# %%
sr.plot()
plt.tick_params(labelbottom=False, labelleft=False)
plt.show()

# %%
sr_new = sr.to_crs(crs)

# %%
sr_new.plot()
plt.tick_params(labelbottom=False, labelleft=False)
plt.show()

# %%
cell.shape

# %%
axs = sr_new.plot()
cell.boundary.plot(color="darkslategrey", linewidth=.2, ax=axs)
axs.tick_params(labelbottom=False, labelleft=False)
plt.show()

# %%
merged = gpd.sjoin(sr_new, cell, how="left")

# %%
merged.head()

# %%
cell.head()

# %%
# compute stats per grid cell
dissolve = merged[["stocking_rate", "index_right", "geometry"]].dissolve(
    by="index_right", aggfunc=np.mean
)
# put this into cell
cell.loc[dissolve.index, "stocking_rate"] = dissolve["stocking_rate"].values

# %%
cell.dropna(inplace=True)

# %%
cell.head()

# %%
plot_transform = cplt.rotated_pole_transform(data)
plt.figure(figsize=(9, 7))
axs = plt.axes(projection=cplt.plot_projection)

# plot data for the variable
data_["T"].plot(
    ax=axs,
    cmap="Spectral_r",
    x="rlon",
    y="rlat",
    robust=True,
    transform=plot_transform
)
cell.to_crs(cplt.plot_projection).plot(
    column="stocking_rate", ax=axs, edgecolor="darkslategrey",
    facecolor="none", linewidth=.5
)

axs.set_title(None)
plt.axis("equal")
plt.tight_layout()
plt.show()

# %%
cellplot_transform = cplt.rotated_pole_transform(data)
plt.figure(figsize=(6, 7))
axs = plt.axes(projection=cplt.plot_projection)
cell.to_crs(cplt.plot_projection).plot(
    column="stocking_rate", cmap="Spectral_r", scheme="equal_interval",
    ax=axs, edgecolor="darkslategrey", linewidth=.2, figsize=(9, 9),
    legend=True, legend_kwds={
        "loc": "upper left", "fmt": "{:.2f}", "title": "Stocking rate"
    }
)
for legend_handle in axs.get_legend().legendHandles:
    legend_handle.set_markeredgewidth(.2)
    legend_handle.set_markeredgecolor("darkslategrey")
plt.axis("equal")
plt.tight_layout()
plt.show()

# %%



