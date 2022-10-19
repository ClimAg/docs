# %% [markdown]
# # ModVege grass growth model (Jouven et al. 2006)
#
# - Jouven, M., Carrère, P. and Baumont, R. (2006). 'Model predicting dynamics
#   of biomass, structure and digestibility of herbage in managed permanent
#   pastures. 1. Model description', *Grass and Forage Science*, vol. 61,
#   no. 2, pp. 112-124. DOI: [10.1111/j.1365-2494.2006.00515.x][Jouven1].
# - Jouven, M., Carrère, P. and Baumont, R. (2006). 'Model predicting dynamics
#   of biomass, structure and digestibility of herbage in managed permanent
#   pastures. 2. Model evaluation', *Grass and Forage Science*, vol. 61, no. 2,
#   pp. 125-133. DOI: [10.1111/j.1365-2494.2006.00517.x][Jouven2].
# - Chemin, Y. (2022). 'modvege', Python. [Online]. Available at
#   <https://github.com/YannChemin/modvege> (Accessed 6 September 2022).
#
# [Jouven1]: https://doi.org/10.1111/j.1365-2494.2006.00515.x
# [Jouven2]: https://doi.org/10.1111/j.1365-2494.2006.00517.x
#
# Running ModVege using the example data provided in
# <https://github.com/YannChemin/modvege>

# %%
import os
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
import xarray as xr
import climag.plot_configs as cplt
from climag.modvege_run import run_modvege

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR = os.path.join("data", "grass-growth", "modvege")

# define the name of the input params file
PARAMS_FILE = os.path.join(DATA_DIR, "params.csv")

# %%
# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_Ireland_ITM")

# %%
# Cork Airport met station coords
LON = -8.48611
LAT = 51.84722

# %% [markdown]
# ## Using example timeseries data

# %%
# define the name of the input timeseries file
TS_FILE = os.path.join(DATA_DIR, "timeseries.csv")

# %%
# run the main function using the example data
run_modvege(
    input_params_file=PARAMS_FILE,
    input_timeseries_file=TS_FILE,
    out_dir=DATA_DIR
)

# %% [markdown]
# ## EURO-CORDEX

# %% [markdown]
# ### rcp85

# %%
# define the name of the input timeseries file
TS_FILE = os.path.join(
    "data", "eurocordex", "IE",
    "evspsblpot_pr_rsds_tas_EUR-11_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_"
    "SMHI-RCA4_v1a_day_20410101-20701231_IE.nc"
)

OUT_DIR = os.path.join(DATA_DIR, "eurocordex", "rcp85")

# %%
# # run the main function using the example data
# run_modvege(
#     input_params_file=PARAMS_FILE,
#     input_timeseries_file=TS_FILE,
#     out_dir=OUT_DIR
# )

# %%
OUT_FILE = os.path.join(
    OUT_DIR,
    "modvege_EUR-11_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_SMHI-RCA4_v1a_day_"
    "20550101-20551231_IE.nc"
)

data = xr.open_dataset(
    OUT_FILE,
    chunks="auto",
    decode_coords="all"
)

# %%
data

# %% [markdown]
# #### Time subset

# %%
data_ie = data.sel(
    time=[
        f"2055-{month}-21T12:00:00.000000000" for month in sorted(
            list(set(data["time"].dt.month.values))
        )
    ]
)

# %%
data_ie

# %%
cplt.plot_facet_map_variables(data_ie, ie)

# %% [markdown]
# #### Point subset

# %%
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

# %%
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
data_ie

# %%
fig, axs = plt.subplots(nrows=6, ncols=3, figsize=(15, 14), sharex=True)

# cycle colours: https://stackoverflow.com/a/53523348
colors = plt.rcParams["axes.prop_cycle"]()

for v, ax in zip(data_ie.data_vars, axs.flat):
    color = next(colors)["color"]
    ax.plot(data_ie["time"].dt.dayofyear, data_ie[v], color=color)
    ax.set_title(
        data_ie[v].attrs["long_name"] + " [" + data_ie[v].attrs["units"] + "]"
    )

fig.supxlabel("Day of the year")

# fig.suptitle(f"ModVege outputs, rcp85 ({LON}, {LAT})")

plt.tight_layout()

plt.show()

# %% [markdown]
# ### historical

# %%
# define the name of the input timeseries file
TS_FILE = os.path.join(
    "data", "eurocordex", "IE",
    "evspsblpot_pr_rsds_tas_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_"
    "SMHI-RCA4_v1a_day_19760101-20051231_IE.nc"
)

OUT_DIR = os.path.join(DATA_DIR, "eurocordex", "historical")

# %%
# # run the main function using the example data
# run_modvege(
#     input_params_file=PARAMS_FILE,
#     input_timeseries_file=TS_FILE,
#     out_dir=OUT_DIR
# )

# %%
OUT_FILE = os.path.join(
    OUT_DIR,
    "modvege_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_SMHI-RCA4_v1a_day_"
    "19900101-19901231_IE.nc"
)

data = xr.open_dataset(
    OUT_FILE,
    chunks="auto",
    decode_coords="all"
)

data

# %% [markdown]
# #### Time subset

# %%
data_ie = data.sel(
    time=[
        f"1990-{month}-21T12:00:00.000000000" for month in sorted(
            list(set(data["time"].dt.month.values))
        )
    ]
)

data_ie

# %%
cplt.plot_facet_map_variables(data_ie, ie)

# %% [markdown]
# #### Point subset

# %%
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

data_ie

# %%
fig, axs = plt.subplots(nrows=6, ncols=3, figsize=(15, 14), sharex=True)

# cycle colours: https://stackoverflow.com/a/53523348
colors = plt.rcParams["axes.prop_cycle"]()

for v, ax in zip(data_ie.data_vars, axs.flat):
    color = next(colors)["color"]
    ax.plot(data_ie["time"].dt.dayofyear, data_ie[v], color=color)
    ax.set_title(
        data_ie[v].attrs["long_name"] + " [" + data_ie[v].attrs["units"] + "]"
    )

fig.supxlabel("Day of the year")

# fig.suptitle(f"ModVege outputs, historical ({LON}, {LAT})")

plt.tight_layout()

plt.show()

# %% [markdown]
# ## HiResIreland

# %% [markdown]
# ### rcp85

# %%
# define the name of the input timeseries file
TS_FILE = os.path.join(
    "data", "HiResIreland", "rcp85",
    "evspsblpot_pr_rsds_tas_COSMO5_MPI-ESM-LR_rcp85_4km.nc"
)

OUT_DIR = os.path.join(DATA_DIR, "hiresireland", "rcp85")

# %%
# # run the main function using the example data
# run_modvege(
#     input_params_file=PARAMS_FILE,
#     input_timeseries_file=TS_FILE,
#     out_dir=OUT_DIR
# )

# %%
OUT_FILE = os.path.join(
    OUT_DIR,
    "modvege_COSMO5_MPI-ESM-LR_rcp85_4km_2055.nc"
)

data = xr.open_dataset(
    OUT_FILE,
    chunks="auto",
    decode_coords="all"
)

data

# %% [markdown]
# #### Time subset

# %%
data_ie = data.sel(
    time=[
        f"2055-{month}-21T10:30:00.000000000" for month in sorted(
            list(set(data["time"].dt.month.values))
        )
    ]
)

data_ie

# %%
cplt.plot_facet_map_variables(data_ie, ie)

# %% [markdown]
# #### Point subset

# %%
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

data_ie

# %%
fig, axs = plt.subplots(nrows=6, ncols=3, figsize=(15, 14), sharex=True)

# cycle colours: https://stackoverflow.com/a/53523348
colors = plt.rcParams["axes.prop_cycle"]()

for v, ax in zip(data_ie.data_vars, axs.flat):
    color = next(colors)["color"]
    ax.plot(data_ie["time"].dt.dayofyear, data_ie[v], color=color)
    ax.set_title(
        data_ie[v].attrs["long_name"] + " [" + data_ie[v].attrs["units"] + "]"
    )

fig.supxlabel("Day of the year")

# fig.suptitle(f"ModVege outputs, rcp85 ({LON}, {LAT})")

plt.tight_layout()

plt.show()
