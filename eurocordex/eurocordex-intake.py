# %% [markdown]
# # intake-esm
#
# - <https://data-infrastructure-services.gitlab-pages.dkrz.de/tutorials-and-use-cases>
# - <https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/>
# - <https://intake-esm.readthedocs.io/>
# - <https://github.com/intake/intake-esm>

# %%
# import libraries
from datetime import datetime, timezone
import cartopy.crs as ccrs
import cordex as cx
import intake
import matplotlib.pyplot as plt

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
dkrz_cat = intake.open_catalog(["https://dkrz.de/s/intake"])

# %%
list(dkrz_cat)

# %%
print(dkrz_cat._entries)

# %%
# view CORDEX metadata
dkrz_cat._entries["dkrz_cordex_disk"]._open_args

# %%
dkrz_cordex = dkrz_cat.dkrz_cordex_disk

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
# filter for EUR-11, historical and rcp85 experiments only, at daily res
query = dict(
    CORDEX_domain="EUR-11",
    driving_model_id="NCC-NorESM1-M",
    experiment_id=["historical", "rcp85"],
    member="r1i1p1",
    model_id="DMI-HIRHAM5",
    rcm_version_id="v3",
    frequency="day",
    variable_id=variables,
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
cordex_eur11.df.to_csv(os.path.join(
    "data", "eurocordex", "cordex_eur11_catalogue.csv"
), index=False)

# %%
# extract data subset
query = dict(
    experiment_id="rcp85",
    variable_id="pr"
)

# %%
cordex_eur11_rcp85_pr = cordex_eur11.search(**query)

# %%
cordex_eur11_rcp85_pr

# %%
cordex_eur11_rcp85_pr.df

# %%
pr = cordex_eur11_rcp85_pr.to_dataset_dict(
    cdf_kwargs=dict(chunks=dict(time=1))
)

# %%
pr

# %%
pr = pr.popitem()[1]

# %%
pr

# %%
pr = pr.isel(time=50)

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
    cbar_label=None,
    transform=ccrs.RotatedPole(
        pole_latitude=cx.domain_info("EUR-11")["pollat"],
        pole_longitude=cx.domain_info("EUR-11")["pollon"]
    )
):

    plt.figure(figsize=(20, 10))
    ax = plt.axes(projection=transform)
    ax.gridlines(
        draw_labels=True,
        linewidth=.5,
        color=grid_color,
        xlocs=range(-180, 180, 10),
        ylocs=range(-90, 90, 5),
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
    ax.coastlines(resolution="50m", color=border_color, linewidth=border_width)
    if title is not None:
        ax.set_title(title)

# %%
data_plot(
    pr["pr"],
    cmap="Blues",
    cbar_label=(
        pr["pr"].attrs["long_name"] + " [" + pr["pr"].attrs["units"] + "]"
    )
)

# %%
# extract data subset
query = dict(
    experiment_id="historical",
    variable_id="pr"
)

# %%
cordex_eur11_rcp85_pr = cordex_eur11.search(**query)

# %%
pr = cordex_eur11_rcp85_pr.to_dataset_dict(
    cdf_kwargs=dict(chunks=dict(time=1))
)

# %%
pr = pr.popitem()[1]

# %%
pr

# %%
pr = pr.isel(time=50)

# %%
data_plot(
    pr["pr"],
    cmap="Blues",
    cbar_label=(
        pr["pr"].attrs["long_name"] + " [" + pr["pr"].attrs["units"] + "]"
    )
)
