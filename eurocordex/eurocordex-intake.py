# %% [markdown]
# # intake-esm
#
# - <https://data-infrastructure-services.gitlab-pages.dkrz.de/tutorials-and-use-cases>
# - <https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/>
# - <https://intake-esm.readthedocs.io/>
# - <https://github.com/intake/intake-esm>

# %%
# import libraries
from datetime import datetime, timezones
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
dkrz_cat = intake.open_catalog(["https://dkrz.de/s/intake"])

# %%
list(dkrz_cat)

# %%
print(dkrz_cat._entries)

# %%
dkrz_cordex = dkrz_cat.dkrz_cordex_disk

# %%
dkrz_cordex

# %%
dkrz_cordex.df.head()

# %%
dkrz_cordex.esmcol_data["description"]

# %%
dkrz_cordex.esmcol_data["catalog_file"]

# %%
list(dkrz_cordex.df.columns)

# %%
# can also be viewed from the top level catalogue
dkrz_cat._entries["dkrz_cordex_disk"]._open_args

# %%
list(dkrz_cordex.df["CORDEX_domain"].unique())

# %%
list(dkrz_cordex.df["experiment_id"].unique())

# %%
list(dkrz_cordex.df["frequency"].unique())

# %%
# filter for EUR-11, historical and rcp85 experiments only, at daily res
query = dict(
    CORDEX_domain=["EUR-11", "EUR-11i"],
    experiment_id=["historical", "rcp85"],
    frequency=["day"]
)

# %%
dkrz_eur11 = dkrz_cordex.search(**query)

# %%
dkrz_eur11.df.head()

# %%
list(dkrz_eur11.df["institute_id"].unique())

# %%
list(dkrz_eur11.df["model_id"].unique())

# %%
list(dkrz_eur11.df["driving_model_id"].unique())
