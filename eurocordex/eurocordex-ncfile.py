# %%
# import libraries
import os
from datetime import datetime, timezone
import cartopy.crs as ccrs
import cordex as cx
import geopandas as gpd
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
# Cork Airport met station coords
lon = -8.48611
lat = 51.84722

# %%
# convert lat/lon to rotated pole coordinates
cds = ccrs.RotatedGeodetic(
    pole_latitude=cx.domain_info("EUR-11")["pollat"],
    pole_longitude=cx.domain_info("EUR-11")["pollon"]
).transform_point(x=lon, y=lat, src_crs=ccrs.Geodetic())

# %%
data_ca = data.sel({"rlat": cds[1], "rlon": cds[0]}, method="nearest")

# %%
data_ca

# %%
plt.figure(figsize=(12, 4))
plt.plot(data_ca["time"], data_ca["tasmin"] - 273.15, marker="o")
plt.xlabel(data_ca["time"].attrs["standard_name"])
plt.ylabel(data_ca["tasmin"].attrs["long_name"] + " [°C]")
plt.title(
    data_ca.attrs["project_id"] + ", " +
    data_ca.attrs["CORDEX_domain"] + ", " +
    data_ca.attrs["driving_model_id"] + ", " +
    data_ca.attrs["driving_model_ensemble_member"] + ", " +
    data_ca.attrs["driving_experiment_name"] + ", " +
    data_ca.attrs["model_id"] + ", " +
    data_ca.attrs["rcm_version_id"] + ", " +
    data_ca.attrs["frequency"] +
    ", (" + str(lon) + ", " + str(lat) + ")"
)
plt.tight_layout()
plt.show()

# %%
data_50 = data.isel(time=50)

# %%
data_50

# %%
def data_plot(
    data,
    cmap="terrain",
    vmin=None,
    vmax=None,
    title=None,
    grid_color="lightslategrey",
    border_color="darkslategrey",
    border_width=.5,
    border_res="50m",
    cbar_label=None,
    transform=ccrs.RotatedPole(
        pole_latitude=cx.domain_info("EUR-11")["pollat"],
        pole_longitude=cx.domain_info("EUR-11")["pollon"]
    ),
    grid_xlocs=range(-180, 180, 10),
    grid_ylocs=range(-90, 90, 5)
):

    plt.figure(figsize=(20, 10))
    ax = plt.axes(projection=transform)
    ax.gridlines(
        draw_labels=True,
        linewidth=.5,
        color=grid_color,
        xlocs=grid_xlocs,
        ylocs=grid_ylocs
    )
    data.plot(
        ax=ax,
        cmap=cmap,
        transform=transform,
        vmin=vmin,
        vmax=vmax,
        x="rlon",
        y="rlat",
        cbar_kwargs={"label": cbar_label}
    )
    ax.coastlines(
        resolution=border_res, color=border_color, linewidth=border_width
    )
    if title is not None:
        ax.set_title(title)

# %%
plot_title = (
    data_50.attrs["project_id"] + ", " +
    data_50.attrs["CORDEX_domain"] + ", " +
    data_50.attrs["driving_model_id"] + ", " +
    data_50.attrs["driving_model_ensemble_member"] + ", " +
    data_50.attrs["driving_experiment_name"] + ", " +
    data_50.attrs["model_id"] + ", " +
    data_50.attrs["rcm_version_id"] + ", " +
    data_50.attrs["frequency"] + ", " +
    str(data_50["time"].coords)[38:57]
)

data_plot(
    data_50["tasmin"] - 273.15,
    cmap="Spectral_r",
    cbar_label=data_50["tasmin"].attrs["long_name"] + " [°C]",
    title=plot_title
)

# Cork Airport marker
# plt.scatter(cds[0], cds[1], s=100, c="darkslategrey", marker="*")

plt.show()

# %%
# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="Boundary_IE_NUTS")

# %%
# clip to Ireland's bounding box with a 10 km buffer
data_ie = data_50.rio.clip(
    ie.envelope.to_crs(2157).buffer(10000).to_crs(data_50.rio.crs)
)

# %%
plot_title = (
    data_ie.attrs["project_id"] + ", " +
    data_ie.attrs["CORDEX_domain"] + ", " +
    data_ie.attrs["driving_model_id"] + ", " +
    data_ie.attrs["driving_model_ensemble_member"] + ", " +
    data_ie.attrs["driving_experiment_name"] + ", " +
    data_ie.attrs["model_id"] + ", " +
    data_ie.attrs["rcm_version_id"] + ", " +
    data_ie.attrs["frequency"] + ", " +
    str(data_ie["time"].coords)[38:57]
)

data_plot(
    data_ie["tasmin"] - 273.15,
    cmap="Spectral_r",
    cbar_label=data_50["tasmin"].attrs["long_name"] + " [°C]",
    title=plot_title,
    border_width=.75,
    border_res="10m",
    grid_xlocs=range(-180, 180, 2),
    grid_ylocs=range(-90, 90, 1)
)

# Cork Airport marker
# plt.scatter(cds[0], cds[1], s=100, c="darkslategrey", marker="*")

plt.show()
