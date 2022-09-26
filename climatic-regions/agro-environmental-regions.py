# %% [markdown]
# # Agro-environmental regions in Ireland
#
# Agro-environmental regions described in Holden and Brereton (2004) derived
# from February rainfall data
#
# A screenshot of the map in the paper was taken and georeferenced into vector
# data
#
# Holden, N. M. and Brereton, A. J. (2004). 'Definition of agroclimatic regions
# in Ireland using hydro-thermal and crop yield data', Agricultural and Forest
# Meteorology, vol. 122, no. 3, pp. 175–191. DOI:
# [10.1016/j.agrformet.2003.09.010][DOI].
#
# [DOI]: https://doi.org/10.1016/j.agrformet.2003.09.010

# %%
# import libraries
import os
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
import climag.plot_configs

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
# define data path
DATA_DIR = os.path.join(
    "data",
    "climatic-regions",
    "agro-environmental-regions",
    "agro-environmental-regions.gpkg"
)

# %%
data = gpd.read_file(DATA_DIR, layer="agro-environmental-regions")

# %%
data

# %%
data.crs

# %%
data.shape

# %%
data.plot(
    column="Cluster",
    legend=True,
    figsize=(9, 9),
    cmap="viridis",
    legend_kwds=dict(loc="upper left")
)
plt.title("Agro-environmental regions in Ireland [Holden and Brereton (2004)]")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
