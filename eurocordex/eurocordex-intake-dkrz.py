# %% [markdown]
# # intake-esm
#
# - <https://data-infrastructure-services.gitlab-pages.dkrz.de/tutorials-and-use-cases>
# - <https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/>
# - <https://intake-esm.readthedocs.io/>
# - <https://github.com/intake/intake-esm>
# - <https://gallery.pangeo.io/repos/pangeo-data/pangeo-tutorial-gallery/intake.html>
# - <https://intake.readthedocs.io/>

# %%
# import libraries
import os
from datetime import datetime, timezone
import intake
import matplotlib.pyplot as plt
import xarray as xr
import climag.plot_configs as cplt

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR_BASE = os.path.join("data", "eurocordex")

# %%
os.makedirs(DATA_DIR_BASE, exist_ok=True)

# %%
# load a dataset to extract metadata
FILE_PATH = os.path.join(
    DATA_DIR_BASE,
    "rcp85",
    "mon",
    "pr_EUR-11_NCC-NorESM1-M_rcp85_r1i1p1_" +
    "DMI-HIRHAM5_v3_mon_204101-205012.nc"
)

data_ec = xr.open_dataset(FILE_PATH, decode_coords="all", chunks=True)

# %% [markdown]
# ## DKRZ intake catalogue

# %%
dkrz_cat = intake.open_catalog(["https://dkrz.de/s/intake"])

# %%
dkrz_cordex = dkrz_cat.dkrz_cordex_disk

# %%
timerange = [
    "19760101-19801231",
    "19810101-19851231",
    "19860101-19901231",
    "19910101-19951231",
    "19960101-20001231",
    "20010101-20051231",
    "20410101-20451231",
    "20460101-20501231",
    "20510101-20551231",
    "20560101-20601231",
    "20610101-20651231",
    "20660101-20701231"
]

# %%
variables = [
    "evspsblpot", "hurs", "huss", "mrso", "pr", "ps",
    "rlds", "rsds", "rlus", "rsus", "sund",
    "tas", "tasmax", "tasmin"
]

# %%
list(dkrz_cat)

# %%
print(dkrz_cat._entries)

# %%
# view CORDEX metadata
dkrz_cat._entries["dkrz_cordex_disk"]._open_args

# %%
dkrz_cordex.esmcol_data["description"]

# %%
dkrz_cordex

# %%
dkrz_cordex.df.head()

# %%
dkrz_cordex.esmcol_data["catalog_file"]

# %%
list(dkrz_cordex.df.columns)

# %%
list(dkrz_cordex.df["CORDEX_domain"].unique())

# %%
list(dkrz_cordex.df["institute_id"].unique())

# %%
list(dkrz_cordex.df["driving_model_id"].unique())

# %%
list(dkrz_cordex.df["experiment_id"].unique())

# %%
list(dkrz_cordex.df["member"].unique())

# %%
list(dkrz_cordex.df["model_id"].unique())

# %%
list(dkrz_cordex.df["rcm_version_id"].unique())

# %%
list(dkrz_cordex.df["frequency"].unique())

# %%
list(dkrz_cordex.df["variable_id"].unique())

# %%
list(dkrz_cordex.df["time_range"].unique())

# %%
# filter for EUR-11, historical and rcp85 experiments only, at daily res
query = dict(
    CORDEX_domain="EUR-11",
    driving_model_id="NCC-NorESM1-M",
    experiment_id="rcp85",
    member="r1i1p1",
    model_id="DMI-HIRHAM5",
    rcm_version_id="v3",
    frequency="day",
    variable_id="pr",
    time_range=timerange
)

# %%
cordex_eur11 = dkrz_cordex.search(**query)

# %%
cordex_eur11

# %%
cordex_eur11.df

# %%
# replace URI to path to downloaded data
cordex_eur11.df["uri"] = (
    "data" + os.sep +
    "eurocordex" + os.sep +
    cordex_eur11.df["experiment_id"] + os.sep +
    "day" + os.sep +
    cordex_eur11.df["uri"].str.split("/").str[-1]
)

# %%
cordex_eur11.df

# %%
pr = cordex_eur11.to_dataset_dict(cdf_kwargs=dict(chunks=dict(time=1)))

# %%
pr

# %%
pr = pr.popitem()[1]

# %%
pr

# %%
pr = pr.isel(time=50)

# %%
FILE_PATH = os.path.join(
    DATA_DIR_BASE,
    "rcp85",
    "mon",
    "pr_EUR-11_NCC-NorESM1-M_rcp85_r1i1p1_" +
    "DMI-HIRHAM5_v3_mon_204101-205012.nc"
)

data_ec = xr.open_dataset(FILE_PATH, decode_coords="all", chunks=True)

# %%
plot_transform = cplt.rotated_pole_transform(pr)
data_var = pr[list(pr.keys())[0]]  # extract variable name
plot_data = data_var * 60 * 60 * 24  # convert to mm/day
cbar_label = data_var.attrs["long_name"] + " [mm/day]"  # colorbar label

plt.figure(figsize=(20, 10))
ax = plt.axes(projection=plot_transform)

# specify gridline spacing and labels
ax.gridlines(
    draw_labels=True,
    xlocs=range(-180, 180, 10),
    ylocs=range(-90, 90, 5),
    color="lightslategrey",
    linewidth=.5
)

# plot data for the variable
plot_data.plot(
    ax=ax,
    cmap="GnBu",
    transform=plot_transform,
    x="rlon",
    y="rlat",
    cbar_kwargs={"label": cbar_label}
)

# add boundaries
ax.coastlines(resolution="50m", color="darkslategrey", linewidth=.5)

ax.set_title(cplt.cordex_plot_title(pr))  # set plot title

plt.show()
