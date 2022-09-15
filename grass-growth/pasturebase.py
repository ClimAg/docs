# %%
import os
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import pandas as pd
import climag.plot_configs

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR = os.path.join("data", "pasturebase", "GrowthRateAveragebyWeek.csv")

# %%
grass_ie = pd.read_csv(DATA_DIR)

# %%
grass_ie.sort_values(by=["Name", "Year", "WeekNo"], inplace=True)

# %%
grass_ie.shape

# %%
list(grass_ie)

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
grass_ie.to_csv(
    os.path.join("data", "pasturebase", "pasturebase.csv"), index=False
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
    os.path.join("data", "pasturebase", "pasturebase_pivot.csv"), index=False
)

# %%
grass_ts.plot(figsize=(16, 6), linewidth=1, cmap="tab20")
plt.title("Grass growth in Ireland based on PastureBase Ireland data")
plt.xlabel("Time")
plt.ylabel("Grass growth (kg DM/ha/d)")
plt.legend(ncol=3)
plt.show()

# %%
for c in list(grass_ts):
    grass_ts[c].plot(figsize=(12, 4), linewidth=1)
    plt.title(
        "Grass growth in Co. " + c + " based on PastureBase Ireland data"
    )
    plt.xlabel("Time")
    plt.ylabel("Grass growth (kg DM/ha/d)")
    plt.show()

# %%
years = list(grass_ts.index.year.unique())
for y in years:
    if y > 2012:
        grass_ts.loc[str(y)].plot(
            figsize=(12, 4), linewidth=1.25, cmap="tab20"
        )
        plt.title(
            "Grass growth per county in " + str(y) +
            " based on PastureBase Ireland data"
        )
        plt.xlabel("Time")
        plt.ylabel("Grass growth (kg DM/ha/d)")
        plt.legend(ncol=6)
        plt.show()
