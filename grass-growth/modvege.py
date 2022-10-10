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
import itertools
import os
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import xarray as xr
import climag.plot_configs as cplt
from climag.modvege_run import run_modvege

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %% [markdown]
# ## Using example timeseries data

# %%
DATA_PATH = os.path.join("data", "grass-growth", "modvege")

# define the name of the input params file
PARAMS_FILE = os.path.join(DATA_PATH, "params.csv")
# define the name of the input timeseries file
TS_FILE = os.path.join(DATA_PATH, "timeseries.csv")
# outputs
OUT_FILE = os.path.join(DATA_PATH, "output.csv")

# %%
# run the main function using the example data
run_modvege(
    input_params_file=PARAMS_FILE,
    input_timeseries_file=TS_FILE,
    out_file=OUT_FILE
)

# %% [markdown]
# ## EURO-CORDEX

# %%
# define the name of the input timeseries file
TS_FILE = os.path.join(
    "data", "eurocordex", "IE",
    "evspsblpot_pr_tas_EUR-11_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_SMHI-RCA4_v1a_"
    "day_20410101-20701231_IE.nc"
)

# outputs
OUT_FILE = os.path.join(
    DATA_PATH,
    "modvege_EUR-11_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_SMHI-RCA4_v1a_"
    "day_20410101-20701231_IE.nc"
)

# %%
# run the main function using the example data
run_modvege(
    input_params_file=PARAMS_FILE,
    input_timeseries_file=TS_FILE,
    out_file=OUT_FILE
)

# %%
data = xr.open_dataset(
    OUT_FILE,
    chunks="auto",
    decode_coords="all"
)

# %%
data

# %%
# subset for a point in time
data_ie = data.isel(time=3458)

# %%
data_ie

# %%
for v in data.data_vars:
    cbar_label = (
        data_ie[v].attrs["long_name"] + " [" + data_ie[v].attrs["units"] + "]"
    )  # colorbar label
    plot_transform = cplt.rotated_pole_transform(data_ie)

    plt.figure(figsize=(20, 10))
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
        cmap="YlGn",
        transform=plot_transform,
        x="rlon",
        y="rlat",
        cbar_kwargs=dict(label=cbar_label)
    )

    # add boundaries
    ax.coastlines(resolution="10m", color="darkslategrey", linewidth=.75)

    ax.set_title(
        "ModVege output, " +
        datetime.strftime(
            datetime.strptime(
                str(data_ie.coords["time"].values)[:10], "%Y-%m-%d"
            ),
            "%-d %b %Y"
        )
    )  # set plot title

    plt.show()

# %%
# point subset
# Cork Airport met station coords
LON = -8.48611
LAT = 51.84722

# %%
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

# %%
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
data_ie

# %%
fig, axs = plt.subplots(nrows=6, ncols=3, figsize=(15, 14))
for v, ax in zip(data_ie.data_vars, itertools.product(range(6), range(3))):
    axs[ax[0], ax[1]].plot(data_ie["time"], data_ie[v])
    axs[ax[0], ax[1]].set_title(
        data_ie[v].attrs["long_name"] + " [" + data_ie[v].attrs["units"] + "]"
    )
fig.suptitle(f"ModVege outputs, rcp85 ({LON}, {LAT})")
plt.tight_layout()
plt.show()
