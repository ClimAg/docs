# %% [markdown]
# # py-cordex
#
# - <https://py-cordex.readthedocs.io/en/stable/domains.html>
# - <https://py-cordex.readthedocs.io/en/stable/prudence.html>
# - <https://data-infrastructure-services.gitlab-pages.dkrz.de/tutorials-and-use-cases/>
# - <http://prudence.dmi.dk/>

# %%
# import libraries
import os
from datetime import datetime, timezone
import cartopy.crs as ccrs
import cartopy.feature as cf
import cordex as cx
import matplotlib.pyplot as plt
import intake

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
cx.domain_info("EUR-11")

# %%
cx.domains.tables.keys()

# %%
cx.domains.table

# %%
eur11 = cx.cordex_domain("EUR-11", dummy="topo")

# %%
eur11

# %%
plt.figure(figsize=(10, 10))
eur11.topo.plot(cmap="terrain")
plt.axis("equal")
plt.show()

# %%
eur11.topo.plot(x="lon", y="lat", cmap="terrain")
plt.show()

# %%
pole = (
    eur11.rotated_latitude_longitude.grid_north_pole_longitude,
    eur11.rotated_latitude_longitude.grid_north_pole_latitude,
)

# %%
pole

# %%
def plot(
    da,
    pole,
    vmin=None,
    vmax=None,
    borders=True,
    title=None,
    transform=ccrs.RotatedPole(pole_latitude=pole[1], pole_longitude=pole[0]),
    projection=ccrs.PlateCarree()
):
    """plot a domain using the right projection with cartopy"""

    plt.figure(figsize=(20, 10))
    ax = plt.axes(projection=transform)
    ax.gridlines(
        draw_labels=True,
        linewidth=.5,
        color="gray",
        xlocs=range(-180, 180, 10),
        ylocs=range(-90, 90, 5),
    )
    da.plot(
        ax=ax,
        cmap="terrain",
        transform=transform,
        vmin=vmin,
        vmax=vmax,
        x="rlon",
        y="rlat",
    )
    ax.coastlines(resolution="50m", color="black", linewidth=1)
    if borders:
        ax.add_feature(cf.BORDERS)
    if title is not None:
        ax.set_title(title)

# %%
plot(eur11.topo, pole)

# %% [markdown]
# ## PRUDENCE regions

# %%
cx.regions.prudence.df

# %%
prudence = cx.regions.prudence.regionmask

# %%
plt.figure(figsize=(10, 10))
proj = ccrs.LambertConformal(central_longitude=15)
ax = prudence.plot(
    add_ocean=True, projection=proj, resolution="50m", label="abbrev"
)
plt.axis("equal")
plt.show()

# %%
mask = cx.regions.prudence.mask_3D(eur11.lon, eur11.lat)

# %%
mask.region

# %%
bi_topo = eur11.topo.where(
    mask.isel(region=(mask.abbrevs == "BI")).squeeze(), drop=True
)

# %%
plot(
    bi_topo,
    pole=pole,
    transform=ccrs.RotatedPole(*pole),
    projection=ccrs.RotatedPole(*pole),
    vmin=-300,
    vmax=1500,
)
