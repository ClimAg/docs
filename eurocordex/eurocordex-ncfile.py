# %%
# import libraries
import os
from datetime import datetime, timezone
import cartopy.crs as ccrs
import cordex as cx
import matplotlib.pyplot as plt
import nc_time_axis
import xarray as xr

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
# configure plot styles
plt.style.use("seaborn-whitegrid")
plt.rcParams["font.family"] = "Source Sans 3"
plt.rcParams["figure.dpi"] = 96
plt.rcParams["axes.grid"] = False
plt.rcParams["text.color"] = "darkslategrey"
plt.rcParams["axes.labelcolor"] = "darkslategrey"
plt.rcParams["xtick.labelcolor"] = "darkslategrey"
plt.rcParams["ytick.labelcolor"] = "darkslategrey"
plt.rcParams["figure.titleweight"] = "semibold"
plt.rcParams["axes.titleweight"] = "semibold"
plt.rcParams["figure.titlesize"] = "13"
plt.rcParams["axes.titlesize"] = "12"
plt.rcParams["axes.labelsize"] = "10"

# %%
DATA_DIR_BASE = os.path.join("data", "eurocordex")

# %%
FILE_PATH = os.path.join(
    DATA_DIR_BASE,
    "historical",
    "mon",
    "tasmin_EUR-11_NCC-NorESM1-M_historical_r1i1p1_" +
    "DMI-HIRHAM5_v3_mon_200101-200512.nc"
)

# %%
data = xr.open_dataset(FILE_PATH, decode_coords="all", chunks=True)

# %%
data

# %%
data["lat"]

# %%
data_ca = data.isel(rlat=51, rlon=-8)

# %%
data_ca

# %%
data_ca.plot.scatter("time", "tasmin", aspect=3, size=4)
plt.tight_layout()
plt.show()

# %%
data_50 = data.isel(time=50)

# %%
data_50

# %%
eur = cx.cordex_domain("EUR-44", dummy="topo")

# %%
pole = (
    eur.rotated_latitude_longitude.grid_north_pole_longitude,
    eur.rotated_latitude_longitude.grid_north_pole_latitude,
)

# %%
def plot(
    da,
    pole,
    cmap="terrain",
    vmin=None,
    vmax=None,
    title=None,
    grid_color="grey",
    transform=ccrs.RotatedPole(pole_latitude=pole[1], pole_longitude=pole[0])
):
    """plot a domain using the right projection with cartopy"""

    plt.figure(figsize=(20, 10))
    ax = plt.axes(projection=transform)
    ax.gridlines(
        draw_labels=True,
        linewidth=.5,
        color=grid_color,
        xlocs=range(-180, 180, 10),
        ylocs=range(-90, 90, 5),
    )
    da.plot(
        ax=ax,
        cmap=cmap,
        transform=transform,
        vmin=vmin,
        vmax=vmax,
        x="rlon",
        y="rlat",
    )
    ax.coastlines(resolution="50m", color="black", linewidth=1)
    if title is not None:
        ax.set_title(title)

# %%
plot(data_50["tasmin"], pole, cmap="Spectral_r")
