# %% [markdown]
# # HiResIreland

# %%
# import libraries
import glob
import itertools
import os
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
import xarray as xr
import climag.plot_configs as cplt

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR_BASE = os.path.join("data", "HiResIreland")

# %%
# Cork Airport met station coords
LON = -8.48611
LAT = 51.84722

# %%
# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_Ireland_ITM")

# %% [markdown]
# ## rcp85

# %%
data = xr.open_mfdataset(
    list(itertools.chain(*list(
        glob.glob(os.path.join(DATA_DIR_BASE, "rcp85", "MPI-ESM-LR", e))
        for e in ["*mean_T_2M*.nc", "*ASOB_S*.nc", "*ET*.nc", "*TOT_PREC*.nc"]
    ))),
    chunks="auto",
    decode_coords="all"
)

# %%
data

# %%
# copy time_bnds
data_time_bnds = data.coords["time_bnds"]

# %%
# copy CRS
data_crs = data.rio.crs

# %%
data_crs

# %% [markdown]
# ### Ireland subset

# %%
# clip to Ireland's boundary
data = data.rio.clip(ie.buffer(1).to_crs(data_crs))

# %%
# reassign time_bnds
data.coords["time_bnds"] = data_time_bnds

# %%
data

# %% [markdown]
# ### Convert units and rename variables

# %%
for v in data.data_vars:
    var_attrs = data[v].attrs  # extract attributes
    if v == "T_2M":
        var_attrs["units"] = "°C"  # convert K to deg C
        data[v] = data[v] - 273.15
        var_attrs["long_name"] = "Near-Surface Air Temperature"
    elif v == "ASOB_S":
        var_attrs["units"] = "MJ m⁻² day⁻¹"  # convert W m-2 to MJ m-2 day-1
        # Allen (1998) - FAO Irrigation and Drainage Paper No. 56 (p. 45)
        # (per second to per day; then convert to mega)
        data[v] = data[v] * (60 * 60 * 24 / 1e6)
        var_attrs["long_name"] = "Surface Net Downwelling Shortwave Radiation"
    elif v == "TOT_PREC":
        var_attrs["units"] = "mm day⁻¹"  # kg m-2 is the same as mm day-1
        var_attrs["long_name"] = "Precipitation"
    else:
        var_attrs["units"] = "mm day⁻¹"
        var_attrs["long_name"] = "Evapotranspiration"
        var_attrs["standard_name"] = "evapotranspiration"
    data[v].attrs = var_attrs  # reassign attributes

# %%
# rename
data = data.rename({
    "T_2M": "tas", "ASOB_S": "rsds", "TOT_PREC": "pr", "w": "evspsblpot"
})

# %%
data

# %% [markdown]
# ### Time subset

# %%
data_ie = data.sel(
    time=[
        str(year) + "-06-21T10:30:00.000000000" for year in sorted(
            list(set(data["time"].dt.year.values))
        )
    ]
)

# %%
data_ie

# %%
for v in data_ie.data_vars:
    cbar_label = (
        data_ie[v].attrs["long_name"] + " [" + data_ie[v].attrs["units"] + "]"
    )  # colorbar label

    if v == "pr":
        cmap = "mako_r"
    elif v == "evspsblpot":
        cmap = "BrBG_r"
    else:
        cmap = "Spectral_r"

    fig = data_ie[v].plot(
        x="lon", y="lat", col="time", col_wrap=5, cmap=cmap, levels=15,
        cbar_kwargs=dict(aspect=40, label=cbar_label), robust=True
    )

    fig.set_xlabels(data_ie["lon"].attrs["standard_name"].capitalize())
    fig.set_ylabels(data_ie["lat"].attrs["standard_name"].capitalize())

    for i, ax in enumerate(fig.axes.flat):
        ie.to_crs(4326).boundary.plot(
            ax=ax, color="darkslategrey", linewidth=.5
        )
        ax.set_title(cplt.hiresireland_date_format(data_ie.isel(time=i)))

    plt.show()

# %%
data_ie = data.sel(time="2055-06-21T10:30:00.000000000")

# %%
data_ie

# %%
for v in data_ie.data_vars:
    cbar_label = (
        data_ie[v].attrs["long_name"] + " [" + data_ie[v].attrs["units"] + "]"
    )  # colorbar label
    if v == "pr":
        cmap = "GnBu"
    elif v == "evspsblpot":
        cmap = "BrBG_r"
    else:
        cmap = "Spectral_r"
    plot_transform = cplt.rotated_pole_transform(data_ie)

    plt.figure(figsize=(7.5, 7))
    ax = plt.axes(projection=plot_transform)

    # specify gridline spacing and labels
    ax.gridlines(
        draw_labels=True,
        xlocs=range(-180, 180, 2),
        ylocs=range(-90, 90, 1),
        color="lightslategrey",
        linewidth=.5
    )

    # plot data for the variable
    data_ie[v].plot(
        ax=ax,
        cmap=cmap,
        transform=plot_transform,
        x="rlon",
        y="rlat",
        levels=15,
        cbar_kwargs=dict(label=cbar_label),
        robust=True
    )

    # add boundaries
    ax.coastlines(resolution="10m", color="darkslategrey", linewidth=.75)

    # ax.set_title(
    #     f"HiResIreland, {data_ie.attrs['title']}, "
    #     f"{data_ie.attrs['frequency']}, {str(data_ie['time'].values)[:10]}"
    # )
    ax.set_title(None)

    plt.axis("equal")
    plt.tight_layout()
    plt.show()

# %% [markdown]
# ### Point subset

# %%
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

# %%
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
data_ie

# %%
for v in data_ie.data_vars:
    plt.figure(figsize=(12, 4))
    plt.plot(data_ie["time"], data_ie[v], linewidth=.5)
    # plt.xlabel(data_ie["time"].attrs["standard_name"].capitalize())
    if v == "rsds":
        ylabel = (
            f"{data_ie[v].attrs['long_name']}\n[{data_ie[v].attrs['units']}]"
        )
    else:
        ylabel = (
            f"{data_ie[v].attrs['long_name']} [{data_ie[v].attrs['units']}]"
        )
    plt.ylabel(ylabel)
    # plt.title(
    #     f"HiResIreland, {data_ie.attrs['title']}, "
    #     f"{data_ie.attrs['frequency']}, ({LON}, {LAT})"
    # )
    plt.tight_layout()
    plt.show()

# %% [markdown]
# ### Export data

# %%
# assign attributes for the data
data.attrs["comment"] = (
    "This dataset has been clipped with the Island of Ireland's boundary. "
    "Last updated: " + str(datetime.now(tz=timezone.utc)) +
    " by nstreethran@ucc.ie."
)

# %%
# reassign CRS
data.rio.write_crs(data_crs, inplace=True)

# %%
data.rio.crs

# %%
data.to_netcdf(os.path.join(
    DATA_DIR_BASE,
    "rcp85",
    "_".join(sorted(list(data.data_vars))) + "_" + data.attrs["title"] + ".nc"
))

# %% [markdown]
# ## historical

# %%
data = xr.open_mfdataset(
    list(itertools.chain(*list(
        glob.glob(os.path.join(DATA_DIR_BASE, "historical", "MPI-ESM-LR", e))
        for e in ["*mean_T_2M*.nc", "*ASOB_S*.nc", "*ET*.nc", "*TOT_PREC*.nc"]
    ))),
    chunks="auto",
    decode_coords="all"
)

# %%
data

# %%
# copy time_bnds
data_time_bnds = data.coords["time_bnds"]

# %%
# copy CRS
data_crs = data.rio.crs

# %%
data_crs

# %% [markdown]
# ### Ireland subset

# %%
# clip to Ireland's boundary
data = data.rio.clip(ie.buffer(1).to_crs(data.rio.crs))

# %%
# reassign time_bnds
data.coords["time_bnds"] = data_time_bnds

# %%
data

# %% [markdown]
# ### Convert units and rename variables

# %%
for v in data.data_vars:
    var_attrs = data[v].attrs  # extract attributes
    if v == "T_2M":
        var_attrs["units"] = "°C"  # convert K to deg C
        data[v] = data[v] - 273.15
        var_attrs["long_name"] = "Near-Surface Air Temperature"
    elif v == "ASOB_S":
        var_attrs["units"] = "MJ m⁻² day⁻¹"  # convert W m-2 to MJ m-2 day-1
        # Allen (1998) - FAO Irrigation and Drainage Paper No. 56 (p. 45)
        # (per second to per day; then convert to mega)
        data[v] = data[v] * (60 * 60 * 24 / 1e6)
        var_attrs["long_name"] = "Surface Net Downwelling Shortwave Radiation"
    elif v == "TOT_PREC":
        var_attrs["units"] = "mm day⁻¹"  # kg m-2 is the same as mm day-1
        var_attrs["long_name"] = "Precipitation"
    else:
        var_attrs["units"] = "mm day⁻¹"
        var_attrs["long_name"] = "Evapotranspiration"
        var_attrs["standard_name"] = "evapotranspiration"
    data[v].attrs = var_attrs  # reassign attributes

# %%
# rename
data = data.rename({
    "T_2M": "tas", "ASOB_S": "rsds", "TOT_PREC": "pr", "w": "evspsblpot"
})

# %%
data

# %% [markdown]
# ### Time subset

# %%
data_ie = data.sel(
    time=[
        str(year) + "-06-21T10:30:00.000000000" for year in sorted(
            list(set(data["time"].dt.year.values))
        )
    ]
)

# %%
data_ie

# %%
for v in data_ie.data_vars:
    cbar_label = (
        data_ie[v].attrs["long_name"] + " [" + data_ie[v].attrs["units"] + "]"
    )  # colorbar label

    if v == "pr":
        cmap = "mako_r"
    elif v == "evspsblpot":
        cmap = "BrBG_r"
    else:
        cmap = "Spectral_r"

    fig = data_ie[v].plot(
        x="lon", y="lat", col="time", col_wrap=5, cmap=cmap, levels=15,
        cbar_kwargs=dict(aspect=40, label=cbar_label), robust=True
    )

    fig.set_xlabels(data_ie["lon"].attrs["standard_name"].capitalize())
    fig.set_ylabels(data_ie["lat"].attrs["standard_name"].capitalize())

    for i, ax in enumerate(fig.axes.flat):
        ie.to_crs(4326).boundary.plot(
            ax=ax, color="darkslategrey", linewidth=.5
        )
        ax.set_title(cplt.hiresireland_date_format(data_ie.isel(time=i)))

    plt.show()

# %%
data_ie = data.sel(time="1990-06-21T10:30:00.000000000")

# %%
data_ie

# %%
for v in data_ie.data_vars:
    cbar_label = (
        data_ie[v].attrs["long_name"] + " [" + data_ie[v].attrs["units"] + "]"
    )  # colorbar label
    if v == "pr":
        cmap = "GnBu"
    elif v == "evspsblpot":
        cmap = "BrBG_r"
    else:
        cmap = "Spectral_r"
    plot_transform = cplt.rotated_pole_transform(data_ie)

    plt.figure(figsize=(7.5, 7))
    ax = plt.axes(projection=plot_transform)

    # specify gridline spacing and labels
    ax.gridlines(
        draw_labels=True,
        xlocs=range(-180, 180, 2),
        ylocs=range(-90, 90, 1),
        color="lightslategrey",
        linewidth=.5
    )

    # plot data for the variable
    data_ie[v].plot(
        ax=ax,
        cmap=cmap,
        transform=plot_transform,
        x="rlon",
        y="rlat",
        levels=15,
        cbar_kwargs=dict(label=cbar_label),
        robust=True
    )

    # add boundaries
    ax.coastlines(resolution="10m", color="darkslategrey", linewidth=.75)

    # ax.set_title(
    #     f"HiResIreland, {data_ie.attrs['title']}, "
    #     f"{data_ie.attrs['frequency']}, {str(data_ie['time'].values)[:10]}"
    # )
    ax.set_title(None)

    plt.axis("equal")
    plt.tight_layout()
    plt.show()

# %% [markdown]
# ### Point subset

# %%
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

# %%
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
data_ie

# %%
for v in data_ie.data_vars:
    plt.figure(figsize=(12, 4))
    plt.plot(data_ie["time"], data_ie[v], linewidth=.5)
    # plt.xlabel(data_ie["time"].attrs["standard_name"].capitalize())
    if v == "rsds":
        ylabel = (
            f"{data_ie[v].attrs['long_name']}\n[{data_ie[v].attrs['units']}]"
        )
    else:
        ylabel = (
            f"{data_ie[v].attrs['long_name']} [{data_ie[v].attrs['units']}]"
        )
    plt.ylabel(ylabel)
    # plt.title(
    #     f"HiResIreland, {data_ie.attrs['title']}, "
    #     f"{data_ie.attrs['frequency']}, ({LON}, {LAT})"
    # )
    plt.tight_layout()
    plt.show()

# %% [markdown]
# ### Export data

# %%
# assign attributes for the data
data.attrs["comment"] = (
    "This dataset has been clipped with the Island of Ireland's boundary. "
    "Last updated: " + str(datetime.now(tz=timezone.utc)) +
    " by nstreethran@ucc.ie."
)

# %%
# reassign CRS
data.rio.write_crs(data_crs, inplace=True)

# %%
data.rio.crs

# %%
data.to_netcdf(os.path.join(
    DATA_DIR_BASE,
    "historical",
    "_".join(sorted(list(data.data_vars))) + "_" + data.attrs["title"] + ".nc"
))
