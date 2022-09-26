# %% [markdown]
# # Seasonality map of Ireland
#
# MODIS-EVI-derived Irish landcover seasonality dataset for 2006
#
# Rory Scarrott (1), Brian O'Connor (1, 2), Ned Dwyer (1), and Fiona Cawkwell
# (2)
#
# (1) Coastal and Marine Research Centre, University College Cork
# (2) Department of Geography, University College Cork
#
# This research was funded by the Irish Environmental Protection Agency under
# grant agreement 2007-CCRP-2.4.
#
# This work is licenced under a Creative Commons Attribution 4.0 International
# Licence
#
# - Scarrott, R. G., O'Connor, B., Dwyer, N. and Cawkwell, F. (2010).
#   'MODIS-EVI-derived Irish landcover seasonality dataset for 2006',
#   Environmental Protection Agency project 2007-CCRP-2.4,
#   University College Cork.
# - O'Connor, B., Scarrott, R. and Dwyer, N. (2013).
#   'Use of remote sensing in phenological research in Ireland',
#   in Donnelly, A. and O'Neill, B. (eds), Climate Change Impacts on Phenology:
#   Implications for Terrestrial Ecosystems,
#   Climate Change Research Programme (CCRP) 2007-2013,
#   Johnstown Castle, Co. Wexford, Ireland,
#   Environmental Protection Agency, pp. 35–39. [Online]. Available at
#   https://www.epa.ie/publications/research/climate-change/climate-change-impacts-on-phenology-implications-for-terrestrial-ecosystems.php
#   (Accessed 19 August 2022).

# %%
# import libraries
import os
from datetime import datetime, timezone
from zipfile import ZipFile
import geopandas as gpd
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import climag.plot_configs

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
# define data directory
DATA_DIR_BASE = os.path.join(
    "data", "climatic-regions", "seasonality-map-epa"
)

# %%
# the ZIP file containing the CLC 2018 data should be moved to this folder
DATA_DIR = os.path.join(DATA_DIR_BASE, "raw")

# %%
os.listdir(DATA_DIR)

# %%
ZIP_FILE = os.path.join(
    DATA_DIR, "2006IESeasonalityDataset_FinalProductPackage.zip"
)

# %%
# list of files/folders in the ZIP archive
ZipFile(ZIP_FILE).namelist()

# %%
data = gpd.read_file(
    f"zip://{ZIP_FILE}!2006IESeasonalityDataset_FinalProductPackage/"
    "IrishSeasonalityMap2006_38Clusters_ScarrottEtAl2010.shp"
)

# %%
data.shape

# %%
data.crs

# %%
data

# %%
# assign clusters to groups as defined in a draft paper by Scarrott et al.
groups = {
    1: 6,
    2: 6,
    3: 7,
    4: 7,
    5: 1,
    6: 7,
    7: 2,
    8: 7,
    9: 8,
    10: 3,
    11: 10,
    12: 7,
    13: 4,
    14: 10,
    15: 8,
    16: 10,
    17: 9,
    18: 10,
    19: 10,
    20: 5,
    21: 9,
    22: 10,
    23: 10,
    24: 10,
    25: 10,
    26: 9,
    27: 10,
    28: 10,
    29: 10,
    30: 10,
    31: 9,
    32: 10,
    33: 10,
    34: 10,
    35: 10,
    36: 10,
    37: 10,
    38: 10
}

# %%
data["Group"] = data["Class"].map(groups)

# %%
# convert column to string for plotting
data["plot_class"] = data["Class"].astype(str).str.zfill(2)
data["Group"] = data["Group"].astype(str).str.zfill(2)

# %%
data

# %%
# new colour map
# https://stackoverflow.com/a/31052741
# sample the colormaps that you want to use. Use 20 from each so we get 40
# colors in total
colors1 = plt.cm.tab20b(np.linspace(0., 1, 20))
colors2 = plt.cm.tab20c(np.linspace(0, 1, 20))

# combine them and build a new colormap
colors = np.vstack((colors1, colors2))

# %%
data.plot(
    column="plot_class",
    legend=True,
    figsize=(9, 9),
    cmap=mcolors.ListedColormap(colors),
    legend_kwds=dict(loc="upper right", bbox_to_anchor=(1.15, 1.05))
)
plt.show()

# %%
data.plot(
    column="Group",
    legend=True,
    figsize=(9, 9),
    cmap="viridis_r",
    legend_kwds=dict(loc="upper right", bbox_to_anchor=(1.15, 1.05))
)
plt.show()
