#!/usr/bin/env python
# coding: utf-8

# # PastureBase Ireland
#
# <https://pasturebase.teagasc.ie>
#
# Hanrahan, L., Geoghegan, A., O'Donovan, M., Griffith, V., Ruelle, E.,
# Wallace, M. and Shalloo, L. (2017). 'PastureBase Ireland: A grassland
# decision support system and national database',
# *Computers and Electronics in Agriculture*, vol. 136, pp. 193-201.
# DOI: [10.1016/j.compag.2017.01.029][Hanrahan].
#
# [Hanrahan]: https://doi.org/10.1016/j.compag.2017.01.029

import os
from datetime import datetime, timezone

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.cbook import boxplot_stats

DATA_DIR = os.path.join(
    "data", "grass_growth", "PastureBaseIreland", "GrowthRateAveragebyWeek.csv"
)

grass = pd.read_csv(DATA_DIR)

grass.head()

grass.shape

list(grass)

grass.sort_values(by=["Name", "Year", "WeekNo"], inplace=True)

# convert year and week number to timestamp
# (Monday as the first day of the week)
grass["Timestamp"] = grass.apply(
    lambda row: datetime.strptime(
        str(row.Year) + "-" + str(row.WeekNo) + "-1", "%G-%V-%u"
    ),
    axis=1,
)

# create time series using counties as individual columns
grass.drop(columns=["Counties_CountyID"], inplace=True)

grass.head()

grass_ts = pd.pivot_table(
    grass[["Name", "AvgGrowth", "Timestamp"]],
    values="AvgGrowth",
    index=["Timestamp"],
    columns=["Name"],
)

grass_ts.shape

grass_ts["time"] = grass_ts.index

grass_ts.sort_values(by=["time"], inplace=True)

grass_ts.head()

# drop NI counties
grass_ts.drop(columns=["Armagh", "Derry", "Down", "Tyrone"], inplace=True)

# use weekly time series starting on Monday to fill missing rows
grass_ = pd.DataFrame(
    pd.date_range(
        str(grass_ts["time"][0].year) + "-01-01",
        str(grass_ts["time"][len(grass_ts) - 1].year) + "-12-31",
        freq="W-MON",
    ),
    columns=["time"],
)

grass_ts = pd.merge(grass_, grass_ts, how="outer")

grass_ts.index = grass_ts["time"]

grass_ts.drop(columns=["time"], inplace=True)

grass_ts.shape

# new colour map
# https://stackoverflow.com/a/31052741
# sample the colormaps that you want to use. Use 15 from each so we get 30
# colors in total
colors1 = plt.cm.tab20b(np.linspace(0.0, 1, 15))
colors2 = plt.cm.tab20c(np.linspace(0, 1, 15))

# combine them and build a new colormap
colors = np.vstack((colors1, colors2))

# ## Distribution

# with outliers
grass_ts.plot.box(
    figsize=(14, 5),
    showmeans=True,
    patch_artist=True,
    color={
        "medians": "Crimson",
        "whiskers": "DarkSlateGrey",
        "caps": "DarkSlateGrey",
    },
    boxprops={"facecolor": "Lavender", "color": "DarkSlateGrey"},
    meanprops={
        "markeredgecolor": "DarkSlateGrey",
        "marker": "d",
        "markerfacecolor": (1, 1, 0, 0),  # transparent
    },
    flierprops={"markeredgecolor": "LightSteelBlue", "zorder": 1},
)
plt.xticks(rotation="vertical")
plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
plt.tight_layout()
# plt.savefig(
#     os.path.join(
#         "data", "grass_growth", "PastureBaseIreland", "boxplot_outliers.png"
#     )
# )
plt.show()

# ## Time series

counties = list(grass_ts)

# pivot table for plotting
grass_piv = grass_ts.copy()
grass_piv["year"] = grass_piv.index.year
grass_piv["weekno"] = grass_piv.index.isocalendar().week
grass_piv = pd.pivot_table(grass_piv, index="weekno", columns="year")

grass_piv.head()

for county in counties:
    grass_piv[county].plot(
        figsize=(12, 4),
        xlabel="Week",
        ylabel="Grass growth [kg DM ha⁻¹ day⁻¹]",
    )
    plt.title(f"PastureBase Ireland grass growth data for Co. {county}")
    plt.legend(title=None)
    plt.tight_layout()
    plt.show()

# ## Filtering outliers in distribution

grass_filter = grass_ts.melt(ignore_index=False)

grass_filter["weekno"] = grass_filter.index.isocalendar().week

grass_filter

# filter all values over 180
grass_filter["value"] = np.where(
    grass_filter["value"] < 180, grass_filter["value"], np.nan
)

# filter all values over 60 when the week number is below 11
grass_filter["value"] = np.where(
    (grass_filter["weekno"] < 11) & (grass_filter["value"] > 60),
    np.nan,
    grass_filter["value"],
)

# filter all values over 40 when the week value is over 47
grass_filter["value"] = np.where(
    (grass_filter["weekno"] > 47) & (grass_filter["value"] > 40),
    np.nan,
    grass_filter["value"],
)

grass_filter

# pivot table for plotting
grass_piv = pd.pivot_table(
    grass_filter[["variable", "value"]].reset_index(),
    values="value",
    index=["time"],
    columns=["variable"],
)
grass_piv["year"] = grass_piv.index.year
grass_piv["weekno"] = grass_piv.index.isocalendar().week
grass_piv = pd.pivot_table(grass_piv, index="weekno", columns="year")

grass_piv.tail()

for county in counties:
    grass_piv[county].plot(
        figsize=(12, 4),
        xlabel="Week",
        ylabel="Grass growth [kg DM ha⁻¹ day⁻¹]",
    )
    plt.title(f"PastureBase Ireland grass growth data for Co. {county}")
    plt.legend(title=None)
    plt.tight_layout()
    plt.show()

# with outliers
grass_piv = pd.pivot_table(
    grass_filter[["variable", "value"]].reset_index(),
    values="value",
    index=["time"],
    columns=["variable"],
)
grass_piv.plot.box(
    figsize=(14, 5),
    showmeans=True,
    patch_artist=True,
    color={
        "medians": "Crimson",
        "whiskers": "DarkSlateGrey",
        "caps": "DarkSlateGrey",
    },
    boxprops={"facecolor": "Lavender", "color": "DarkSlateGrey"},
    meanprops={
        "markeredgecolor": "DarkSlateGrey",
        "marker": "d",
        "markerfacecolor": (1, 1, 0, 0),  # transparent
    },
    flierprops={"markeredgecolor": "LightSteelBlue", "zorder": 1},
)
plt.xticks(rotation="vertical")
plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
plt.tight_layout()
# plt.savefig(
#     os.path.join(
#         "data", "grass_growth", "PastureBaseIreland", "boxplot_outliers.png"
#     )
# )
plt.show()

grass_filter = grass_filter.rename(columns={"variable": "county"})
grass_filter.to_csv(
    os.path.join(
        "data", "grass_growth", "PastureBaseIreland", "pasturebase_cleaned.csv"
    )
)

print("Last updated:", datetime.now(tz=timezone.utc))

### Using boxplot stats

# grass_out = grass_ts.copy()
# for col in counties:
#     grass_out[[col]] = grass_out[[col]].replace(
#         list(boxplot_stats(grass_out[[col]].dropna())[0]["fliers"]), np.nan
#     )

# grass_out.plot.box(
#     figsize=(14, 5), showmeans=True, patch_artist=True,
#     color={
#         "medians": "Crimson",
#         "whiskers": "DarkSlateGrey",
#         "caps": "DarkSlateGrey"
#     },
#     boxprops={"facecolor": "Lavender", "color": "DarkSlateGrey"},
#     meanprops={
#         "markeredgecolor": "DarkSlateGrey",
#         "marker": "d",
#         "markerfacecolor": (1, 1, 0, 0)  # transparent
#     },
#     flierprops={"markeredgecolor": "LightSteelBlue", "zorder": 1}
# )
# plt.xticks(rotation="vertical")
# plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
# plt.tight_layout()
# # plt.savefig(
# #     os.path.join("data", "grass_growth", "PastureBaseIreland", "boxplot.png")
# # )
# plt.show()

# grass_out.diff().hist(figsize=(15, 18), bins=50, grid=False)
# plt.tight_layout()
# plt.savefig(
#     os.path.join("data", "grass_growth", "PastureBaseIreland", "diff_hist.png")
# )
# plt.show()

### Filtering outliers using 3-week moving average

# grass_out = grass_ts.reset_index()

# for county in counties:
#     mn = grass_out.rolling(3, center=True, on="time")[county].median()
#     # mn = grass_out.rolling(3, center=True, on="time")[county].mean()
#     # sd = grass_out.rolling(3, center=True, on="time")[county].std()
#     grass_out[f"{county}_outlier"] = (
#         grass_out[county].sub(mn).abs().gt(25)
#     )
#     grass_out[f"{county}_mn"] = mn
#     # grass_out[f"{county}_sd"] = sd
#     # grass_out[f"{county}_f"] = np.nan
#     # grass_out[f"{county}_f"] = grass_out[
#     #     (
#     #         grass_out[county] <=
#     #         grass_out[f"{county}_mn"] + 2 * grass_out[f"{county}_sd"]
#     #     ) & (
#     #         grass_out[county] >=
#     #         grass_out[f"{county}_mn"] - 2 * grass_out[f"{county}_sd"]
#     #     )
#     # ][[county]]
#     # grass_out[f"{county}_f"] = grass_out[
#     #     grass_out[f"{county}_f"].isna()
#     # ][[county]]

# grass_out.set_index("time", inplace=True)

# for county in counties:
#     axs = grass_out.plot(
#         # ylim=[0.0, 200.0],
#         figsize=(10, 4), y=county, label="growth"
#     )
#     grass_out.plot(
#         figsize=(10, 4), y=f"{county}_mn", ax=axs, label="moving_avg",
#         color="orange", zorder=1
#     )
#     # grass_out.plot(
#     #     figsize=(10, 4), y=f"{county}_f", ax=axs, label="f",
#     #     color="purple", linewidth=0.0, marker="*"
#     # )
#     if True in list(grass_out[f"{county}_outlier"].unique()):
#         grass_out[grass_out[f"{county}_outlier"] == True].plot(
#             ax=axs, linewidth=0.0, marker="*", y=county, label="outlier",
#             color="crimson"
#         )
#     plt.title(f"PastureBase Ireland grass growth data for Co. {county}")
#     plt.xlabel("")
#     plt.tight_layout()
#     plt.show()

# for county in counties:
#     axs = grass_out.plot(
#         # ylim=[0.0, 200.0],
#         figsize=(10, 4), y=county, label="growth"
#     )
#     grass_out.plot(
#         figsize=(10, 4), y=f"{county}_mn", ax=axs, label="moving_avg",
#         color="orange", zorder=1
#     )
#     if True in list(grass_out[f"{county}_outlier"].unique()):
#         grass_out[grass_out[f"{county}_outlier"] == True].plot(
#             ax=axs, linewidth=0.0, marker="*", y=county, label="outlier",
#             color="crimson"
#         )
#     plt.title(f"PastureBase Ireland grass growth data for Co. {county}")
#     plt.xlabel("")
#     plt.tight_layout()
#     plt.show()

# for county in counties:
#     axs = grass_out.loc["2017":"2019"].plot(
#         ylim=[0.0, 150.0],
#         figsize=(12, 8), y=county, label="growth"
#     )
#     grass_out.loc["2017":"2019"].plot(
#         figsize=(10, 4), y=f"{county}_mn", ax=axs, label="moving_avg",
#         color="orange", zorder=1
#     )
#     if True in list(
#         grass_out[f"{county}_outlier"].loc["2017":"2019"].unique()
#     ):
#         grass_out[
#             grass_out[f"{county}_outlier"] == True
#         ].loc["2017":"2019"].plot(
#             ax=axs, linewidth=0.0, marker="*", y=county, label="outlier",
#             color="crimson"
#         )
#     plt.title(f"PastureBase Ireland grass growth data for Co. {county}")
#     plt.xlabel("")
#     plt.tight_layout()
#     plt.show()
