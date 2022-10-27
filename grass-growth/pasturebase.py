# %% [markdown]
# # PastureBase Ireland
#
# <https://pasturebase.teagasc.ie>
#
# Hanrahan, L., Geoghegan, A., O'Donovan, M., Griffith, V., Ruelle, E.,
# Wallace, M. and Shalloo, L. (2017). 'PastureBase Ireland: A grassland
# decision support system and national database',
# *Computers and Electronics in Agriculture*, vol. 136, pp. 193–201.
# DOI: [10.1016/j.compag.2017.01.029][Hanrahan].
#
# [Hanrahan]: https://doi.org/10.1016/j.compag.2017.01.029

# %%
import os
from datetime import datetime, timezone
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR = os.path.join(
    "data", "grass-growth", "pasturebase", "GrowthRateAveragebyWeek.csv"
)

# %%
grass_ie = pd.read_csv(DATA_DIR)

# %%
grass_ie.shape

# %%
list(grass_ie)

# %%
grass_ie.sort_values(by=["Name", "Year", "WeekNo"], inplace=True)

# %%
# convert year and week number to timestamp
# (Monday as the first day of the week)
grass_ie["Timestamp"] = grass_ie.apply(
    lambda row: datetime.strptime(
        str(row.Year) + "-" + str(row.WeekNo) + "-1", "%G-%V-%u"
    ),
    axis=1
)

# %%
# create time series using counties as individual columns
grass_ts = grass_ie.drop(columns=["Counties_CountyID", "Year", "WeekNo"])

# %%
grass_ts = pd.pivot_table(
    grass_ts, values="AvgGrowth", index=["Timestamp"], columns=["Name"]
)

# %%
grass_ts.shape

# %%
grass_ts["time"] = grass_ts.index

# %%
grass_ts.sort_values(by=["time"], inplace=True)

# %%
# use weekly time series starting on Monday to fill missing rows
grass_time = pd.DataFrame(
    pd.date_range(
        str(grass_ts["time"][0].year) + "-01-01",
        str(grass_ts["time"][len(grass_ts) - 1].year) + "-12-31",
        freq="W-MON"
    ),
    columns=["time"]
)

# %%
grass_ts = pd.merge(grass_time, grass_ts, how="outer")

# %%
grass_ts.index = grass_ts["time"]

# %%
grass_ts.drop(columns=["time"], inplace=True)

# %%
grass_ts.shape

# %%
grass_ts.to_csv(
    os.path.join("data", "grass-growth", "pasturebase", "pasturebase.csv")
)

# %%
# new colour map
# https://stackoverflow.com/a/31052741
# sample the colormaps that you want to use. Use 15 from each so we get 30
# colors in total
colors1 = plt.cm.tab20b(np.linspace(0., 1, 15))
colors2 = plt.cm.tab20c(np.linspace(0, 1, 15))

# combine them and build a new colormap
colors = np.vstack((colors1, colors2))

# %%
grass_ts.plot(
    figsize=(14, 5), linewidth=1, cmap=mcolors.ListedColormap(colors)
)
plt.ylim(0, 120)
plt.title("Grass growth in Ireland [Data: PastureBase Ireland (Teagasc)]")
plt.xlabel("")
plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
plt.legend(ncol=2)
plt.show()

# %%
for c in list(grass_ts):
    grass_ts[c].plot(figsize=(12, 4), linewidth=1)
    plt.title(
        f"Grass growth in Co. {c} [Data: PastureBase Ireland (Teagasc)]"
    )
    plt.xlabel("")
    plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
    plt.show()

# %%
years = list(grass_ts.index.year.unique())
for y in years:
    if y > 2012:
        grass_ts.loc[str(y)].plot(
            figsize=(12, 4),
            linewidth=1.25,
            cmap=mcolors.ListedColormap(colors)
        )
        plt.title(
            f"Grass growth in Ireland in {y} "
            "[Data: PastureBase Ireland (Teagasc)]"
        )
        plt.xlabel("")
        plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
        plt.legend(ncol=6)
        plt.show()
