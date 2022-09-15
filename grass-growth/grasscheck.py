# %% [markdown]
# # GrassCheck NI
#
# <https://agrisearch.org/grasscheck>

# %%
import os
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import pandas as pd
import climag.plot_configs

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR = os.path.join("data", "grasscheck", "grasscheck.csv")

# %%
grass_ni = pd.read_csv(DATA_DIR, parse_dates=["week"], dayfirst=True)

# %%
# use weekly time series starting on Monday to fill missing rows
grass_ts = pd.DataFrame(
    pd.date_range(
        str(grass_ni["week"][0].year) + "-01-01",
        str(grass_ni["week"][len(grass_ni) - 1].year) + "-12-31",
        freq="W-MON"
    ),
    columns=["week"]
)

# %%
grass_ts = pd.merge(grass_ts, grass_ni, how="outer")

# %%
# save time series
grass_ts.to_csv(DATA_DIR, index=False)

# %%
# set timestamps as the index
grass_ts.index = grass_ts["week"]

# %%
grass_ts.drop(columns=["week"], inplace=True)

# %%
# capitalise county names
counties = []
for c in list(grass_ts):
    counties.append(c.capitalize())

# %%
grass_ts.columns = counties

# %%
grass_ts.plot(figsize=(12, 4), linewidth=1)
plt.title("Grass growth data for Northern Ireland from GrassCheck NI")
plt.xlabel("Time")
plt.ylabel("Grass growth (kg DM/ha/d)")
plt.show()

# %%
for c in counties:
    grass_ts[c].plot(figsize=(12, 4), linewidth=1)
    plt.title(
        "Grass growth data for Co. " + c +
        " from GrassCheck NI"
    )
    plt.xlabel("Time")
    plt.ylabel("Grass growth (kg DM/ha/d)")
    plt.show()

# %%
years = list(grass_ts.index.year.unique())
for y in years:
    grass_ts.loc[str(y)].plot(figsize=(12, 4), linewidth=1.25)
    plt.title(
        "Grass growth data for Northern Ireland in " + str(y) +
        " from GrassCheck NI"
    )
    plt.xlabel("Time")
    plt.ylabel("Grass growth (kg DM/ha/d)")
    plt.show()
