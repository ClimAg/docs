# %%
# import libraries
import os
from datetime import datetime, timezone
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
    "pastdata",
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
plt.figure(figsize=(10, 10))
data_50["tasmin"].plot(cmap="Spectral_r")
plt.axis("equal")
plt.show()
