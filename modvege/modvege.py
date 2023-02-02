# %% [markdown]
# # ModVege grass growth model (Jouven et al. 2006) with EURO-CORDEX data
#
# - Jouven, M., Carrère, P., and Baumont, R. (2006a). 'Model predicting
#   dynamics of biomass, structure and digestibility of herbage in managed
#   permanent pastures. 1. Model description', *Grass and Forage Science*,
#   vol. 61, no. 2, pp. 112-124. DOI:
#   [10.1111/j.1365-2494.2006.00515.x][Jouven1].
# - Jouven, M., Carrère, P., and Baumont, R. (2006b). 'Model predicting
#   dynamics of biomass, structure and digestibility of herbage in managed
#   permanent pastures. 2. Model evaluation', *Grass and Forage Science*,
#   vol. 61, no. 2, pp. 125-133. DOI:
#   [10.1111/j.1365-2494.2006.00517.x][Jouven2].
# - Chemin, Y. (2022). 'modvege', Python. [Online]. Available at
#   <https://github.com/YannChemin/modvege> (Accessed 6 September 2022).
#
# [Jouven1]: https://doi.org/10.1111/j.1365-2494.2006.00515.x
# [Jouven2]: https://doi.org/10.1111/j.1365-2494.2006.00517.x

# %%
import os
import glob
from datetime import datetime, timezone
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import xarray as xr
import climag.plot_configs as cplt
from climag.modvege_run import run_modvege

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR = os.path.join("data", "ModVege")

# define the name of the input params file
PARAMS_FILE = os.path.join(DATA_DIR, "params.csv")

# %%
# Ireland boundary
GPKG_BOUNDARY = os.path.join(
    "data", "boundaries", "NUTS2021", "NUTS_2021.gpkg"
)
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")

# %%
# Valentia Observatory met station coords
LON = -10.24333
LAT = 51.93806

# %%
# define the name of the input time series file
TS_FILE = os.path.join(
    "data", "EURO-CORDEX", "IE",
    "IE_EUR-11_ICHEC-EC-EARTH_rcp85_r12i1p1_SMHI-RCA4_v1_day_"
    "20410101-20701231.nc"
)

# %%
# run the main function using the example data
run_modvege(
    input_params_file=PARAMS_FILE,
    input_timeseries_file=TS_FILE,
    out_dir=DATA_DIR
)

# %%
data = xr.open_mfdataset(
    glob.glob(
        os.path.join(
            DATA_DIR, "EURO-CORDEX", "rcp85", "ICHEC-EC-EARTH", "*.nc"
        )
    ),
    chunks="auto",
    decode_coords="all"
)

# %%
data

# %% [markdown]
# ## Time subset

# %%
data_ie = data.sel(
    time=[
        f"2056-{month}-15T12:00:00.000000000" for month in sorted(
            list(set(data["time"].dt.month.values))
        )
    ]
)

# %%
data_ie

# %% [markdown]
# ### Results

# %%
cplt.plot_facet_map_variables(data_ie, ie)

# %% [markdown]
# ## Point subset

# %%
cds = cplt.rotated_pole_point(data=data, lon=LON, lat=LAT)

# %%
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

# %%
data_ie

# %% [markdown]
# ### Cork Airport met station

# %%
data_ie_df = pd.DataFrame({"time": data_ie["time"]})
for var in data_ie.data_vars:
    data_ie_df[var] = data_ie[var]

data_ie_df.set_index("time", inplace=True)

# configure plot title
plot_title = []
for var in data_ie.data_vars:
    plot_title.append(
        f"{data_ie[var].attrs['long_name']} [{data_ie[var].attrs['units']}]"
    )

data_ie_df.plot(
    subplots=True, layout=(5, 3), figsize=(15, 10),
    legend=False, xlabel="", title=plot_title
)

plt.tight_layout()
plt.show()

# %% [markdown]
# ### Near Derry, NI

# %%
cds = cplt.rotated_pole_point(data=data, lon=-7.297, lat=54.976)
data_ie = data.sel({"rlon": cds[0], "rlat": cds[1]}, method="nearest")

data_ie_df = pd.DataFrame({"time": data_ie["time"]})
for var in data_ie.data_vars:
    data_ie_df[var] = data_ie[var]

data_ie_df.set_index("time", inplace=True)

# configure plot title
plot_title = []
for var in data_ie.data_vars:
    plot_title.append(
        f"{data_ie[var].attrs['long_name']} [{data_ie[var].attrs['units']}]"
    )

data_ie_df.plot(
    subplots=True, layout=(5, 3), figsize=(15, 10),
    legend=False, xlabel="", title=plot_title
)

plt.tight_layout()
plt.show()
