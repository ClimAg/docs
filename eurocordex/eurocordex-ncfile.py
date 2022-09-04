# %% [markdown]
# # EURO-CORDEX data from NC files

# %%
# import libraries
import os
from datetime import datetime, timezone
import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib.pyplot as plt
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
# convert lat/lon to rotated pole coordinates
def rotated_pole_point(data, lon, lat):
    pole_latitude = (
        data.rio.crs.to_dict(
            projjson=True
        )["conversion"]["parameters"][0]["value"]
    )
    pole_longitude = (
        data.rio.crs.to_dict(
            projjson=True
        )["conversion"]["parameters"][1]["value"]
    )
    rp_cds = ccrs.RotatedGeodetic(
        pole_latitude=pole_latitude, pole_longitude=pole_longitude,
    ).transform_point(x=lon, y=lat, src_crs=ccrs.Geodetic())
    return rp_cds[0], rp_cds[1]

# %%
# Cork Airport met station coords
LON = -8.48611
LAT = 51.84722

# %%
# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="Boundary_IE_NUTS_ITM")

# %%
def data_plot(
    data,
    cmap="terrain",
    vmin=None,
    vmax=None,
    grid_color="lightslategrey",
    border_color="darkslategrey",
    border_width=.5,
    border_res="50m",
    cbar_label=None,
    transform=None,
    grid_xlocs=range(-180, 180, 10),
    grid_ylocs=range(-90, 90, 5),
    plot_title=None,
    plot_figsize=(20, 10)
):
    plt.figure(figsize=plot_figsize)
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
    if plot_title is not None:
        ax.set_title(plot_title)

# %%
def cordex_plot_title(data):
    if data.attrs["frequency"] == "mon":
        date_format = "%b %Y"
    elif data.attrs["frequency"] == "day":
        date_format = "%-d %b %Y"
    else:
        date_format = "%Y-%m-%d %H:%M:%S"
    plot_title = (
        data.attrs["project_id"] + ", " +
        data.attrs["CORDEX_domain"] + ", " +
        data.attrs["driving_model_id"] + ", " +
        data.attrs["driving_model_ensemble_member"] + ", " +
        data.attrs["driving_experiment_name"] + ", " +
        data.attrs["model_id"] + ", " +
        data.attrs["rcm_version_id"] + ", " +
        data.attrs["frequency"] + ", " +
        datetime.strftime(
            datetime.fromisoformat(str(data["time"].values)), date_format
        )
    )
    return plot_title

# %%
def rotated_pole_transform(data):
    pole_latitude = (
        data.rio.crs.to_dict(
            projjson=True
        )["conversion"]["parameters"][0]["value"]
    )
    pole_longitude = (
        data.rio.crs.to_dict(
            projjson=True
        )["conversion"]["parameters"][1]["value"]
    )
    transform = ccrs.RotatedPole(
        pole_latitude=pole_latitude, pole_longitude=pole_longitude
    )
    return transform

# %% [markdown]
# ## tasmin

# %%
FILE_PATH = os.path.join(
    DATA_DIR_BASE,
    "historical",
    "mon",
    "tasmin_EUR-11_NCC-NorESM1-M_historical_r1i1p1_" +
    "DMI-HIRHAM5_v3_mon_200101-200512.nc"
)

# %%
data_ec = xr.open_dataset(FILE_PATH, decode_coords="all", chunks=True)

# %%
data_ec

# %%
# extract time series for Cork Airport
cds = rotated_pole_point(data_ec, lon=LON, lat=LAT)
data_ca = data_ec.sel({"rlat": cds[1], "rlon": cds[0]}, method="nearest")

# %%
data_ca

# %%
plt.figure(figsize=(12, 4))
plt.plot(
    data_ca["time"], data_ca[list(data_ca.keys())[0]] - 273.15, marker="o"
)
plt.xlabel(data_ca["time"].attrs["standard_name"])
plt.ylabel(data_ca[list(data_ca.keys())[0]].attrs["long_name"] + " [°C]")
plt.title(
    data_ca.attrs["project_id"] + ", " +
    data_ca.attrs["CORDEX_domain"] + ", " +
    data_ca.attrs["driving_model_id"] + ", " +
    data_ca.attrs["driving_model_ensemble_member"] + ", " +
    data_ca.attrs["driving_experiment_name"] + ", " +
    data_ca.attrs["model_id"] + ", " +
    data_ca.attrs["rcm_version_id"] + ", " +
    data_ca.attrs["frequency"] +
    ", (" + str(LON) + ", " + str(LAT) + ")"
)
plt.tight_layout()
plt.show()

# %%
# extract data for a given time
data_50 = data_ec.isel(time=50)

# %%
data_50

# %%
data_plot(
    data_50[list(data_50.keys())[0]] - 273.15,
    cmap="Spectral_r",
    cbar_label=data_50[list(data_50.keys())[0]].attrs["long_name"] + " [°C]",
    plot_title=cordex_plot_title(data_50),
    transform=rotated_pole_transform(data_50)
)
plt.show()

# %%
# clip to Ireland's bounding box with a 10 km buffer
data_ie = data_50.rio.clip(
    ie.envelope.buffer(10000).to_crs(data_50.rio.crs)
)

# %%
data_plot(
    data_ie[list(data_ie.keys())[0]] - 273.15,
    cmap="Spectral_r",
    cbar_label=data_ie[list(data_ie.keys())[0]].attrs["long_name"] + " [°C]",
    plot_title=cordex_plot_title(data_ie),
    transform=rotated_pole_transform(data_ie),
    border_width=.75,
    border_res="10m",
    grid_xlocs=range(-180, 180, 2),
    grid_ylocs=range(-90, 90, 1)
)

# Cork Airport marker
# plt.scatter(cds[0], cds[1], s=100, c="darkslategrey", marker="*")

plt.show()

# %% [markdown]
# ## tasmax

# %%
FILE_PATH = os.path.join(
    DATA_DIR_BASE,
    "historical",
    "mon",
    "tasmax_EUR-11_NCC-NorESM1-M_historical_r1i1p1_" +
    "DMI-HIRHAM5_v3_mon_200101-200512.nc"
)

data_ec = xr.open_dataset(FILE_PATH, decode_coords="all", chunks=True)

cds = rotated_pole_point(data_ec, lon=LON, lat=LAT)
data_ca = data_ec.sel({"rlat": cds[1], "rlon": cds[0]}, method="nearest")

# %%
plt.figure(figsize=(12, 4))
plt.plot(
    data_ca["time"], data_ca[list(data_ca.keys())[0]] - 273.15, marker="o"
)
plt.xlabel(data_ca["time"].attrs["standard_name"])
plt.ylabel(data_ca[list(data_ca.keys())[0]].attrs["long_name"] + " [°C]")
plt.title(
    data_ca.attrs["project_id"] + ", " +
    data_ca.attrs["CORDEX_domain"] + ", " +
    data_ca.attrs["driving_model_id"] + ", " +
    data_ca.attrs["driving_model_ensemble_member"] + ", " +
    data_ca.attrs["driving_experiment_name"] + ", " +
    data_ca.attrs["model_id"] + ", " +
    data_ca.attrs["rcm_version_id"] + ", " +
    data_ca.attrs["frequency"] +
    ", (" + str(LON) + ", " + str(LAT) + ")"
)
plt.tight_layout()
plt.show()

# %%
data_50 = data_ec.isel(time=50)

# %%
data_plot(
    data_50[list(data_50.keys())[0]] - 273.15,
    cmap="Spectral_r",
    cbar_label=data_50[list(data_50.keys())[0]].attrs["long_name"] + " [°C]",
    plot_title=cordex_plot_title(data_50),
    transform=rotated_pole_transform(data_50)
)
plt.show()

# %%
data_ie = data_50.rio.clip(
    ie.envelope.buffer(10000).to_crs(data_50.rio.crs)
)

# %%
data_plot(
    data_ie[list(data_ie.keys())[0]] - 273.15,
    cmap="Spectral_r",
    cbar_label=data_ie[list(data_ie.keys())[0]].attrs["long_name"] + " [°C]",
    plot_title=cordex_plot_title(data_ie),
    transform=rotated_pole_transform(data_ie),
    border_width=.75,
    border_res="10m",
    grid_xlocs=range(-180, 180, 2),
    grid_ylocs=range(-90, 90, 1)
)
plt.show()

# %% [markdown]
# ## pr

# %%
FILE_PATH = os.path.join(
    DATA_DIR_BASE,
    "rcp85",
    "mon",
    "pr_EUR-11_NCC-NorESM1-M_rcp85_r1i1p1_" +
    "DMI-HIRHAM5_v3_mon_204101-205012.nc"
)

data_ec = xr.open_dataset(FILE_PATH, decode_coords="all", chunks=True)

cds = rotated_pole_point(data_ec, lon=LON, lat=LAT)

# %%
data_ca = data_ec.sel({"rlat": cds[1], "rlon": cds[0]}, method="nearest")

# %%
plt.figure(figsize=(12, 4))
plt.plot(
    data_ca["time"],
    data_ca[list(data_ca.keys())[0]] * 60 * 60 * 24,
    marker="o"
)
plt.xlabel(data_ca["time"].attrs["standard_name"])
plt.ylabel(data_ca[list(data_ca.keys())[0]].attrs["long_name"] + " [mm/day]")
plt.title(
    data_ca.attrs["project_id"] + ", " +
    data_ca.attrs["CORDEX_domain"] + ", " +
    data_ca.attrs["driving_model_id"] + ", " +
    data_ca.attrs["driving_model_ensemble_member"] + ", " +
    data_ca.attrs["driving_experiment_name"] + ", " +
    data_ca.attrs["model_id"] + ", " +
    data_ca.attrs["rcm_version_id"] + ", " +
    data_ca.attrs["frequency"] +
    ", (" + str(LON) + ", " + str(LAT) + ")"
)
plt.tight_layout()
plt.show()

# %%
data_50 = data_ec.isel(time=50)

# %%
data_plot(
    data_50[list(data_50.keys())[0]] * 60 * 60 * 24,
    cmap="viridis_r",
    cbar_label=(
        data_50[list(data_50.keys())[0]].attrs["long_name"] + " [mm/day]"
    ),
    plot_title=cordex_plot_title(data_50),
    transform=rotated_pole_transform(data_50)
)
plt.show()

# %%
data_ie = data_50.rio.clip(
    ie.envelope.buffer(10000).to_crs(data_50.rio.crs)
)

# %%
data_plot(
    data_ie[list(data_ie.keys())[0]] * 60 * 60 * 24,
    cmap="viridis_r",
    cbar_label=(
        data_ie[list(data_ie.keys())[0]].attrs["long_name"] + " [mm/day]"
    ),
    plot_title=cordex_plot_title(data_ie),
    transform=rotated_pole_transform(data_ie),
    border_width=.75,
    border_res="10m",
    grid_xlocs=range(-180, 180, 2),
    grid_ylocs=range(-90, 90, 1)
)
plt.show()
