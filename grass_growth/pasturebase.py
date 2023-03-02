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
from matplotlib.cbook import boxplot_stats
import numpy as np
import pandas as pd

print("Last updated:", datetime.now(tz=timezone.utc))

DATA_DIR = os.path.join(
    "data", "grass_growth", "pasturebase", "GrowthRateAveragebyWeek.csv"
)

grass_ts = pd.read_csv(DATA_DIR)

grass_ts.head()

grass_ts.shape

list(grass_ts)

grass_ts.sort_values(by=["Name", "Year", "WeekNo"], inplace=True)

# convert year and week number to timestamp
# (Monday as the first day of the week)
grass_ts["Timestamp"] = grass_ts.apply(
    lambda row: datetime.strptime(
        str(row.Year) + "-" + str(row.WeekNo) + "-1", "%G-%V-%u"
    ),
    axis=1,
)

# create time series using counties as individual columns
grass_ts.drop(columns=["Counties_CountyID", "Year", "WeekNo"], inplace=True)

grass_ts = pd.pivot_table(
    grass_ts, values="AvgGrowth", index=["Timestamp"], columns=["Name"]
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

grass_ts.to_csv(
    os.path.join("data", "grass_growth", "pasturebase", "pasturebase.csv")
)

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
# plt.savefig(os.path.join("data", "grass_growth", "pasturebase", "boxplot_outliers.png"))
plt.show()

# with outliers
grass_ts.plot.box(
    figsize=(14, 5),
    showmeans=True,
    patch_artist=True,
    ylim=[-5.0, 150.0],
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
# plt.savefig(os.path.join("data", "grass_growth", "pasturebase", "boxplot_outliers.png"))
plt.show()

grass_ts.diff().hist(figsize=(15, 18), bins=50, grid=False)
plt.tight_layout()
# plt.savefig(os.path.join("data", "grass_growth", "pasturebase", "diff_hist_outliers.png"))
plt.show()

# ## Time series

years = list(grass_ts.index.year.unique())
for y in years:
    if y > 2012:
        grass_ts.loc[str(y)].set_index(
            grass_ts.loc[str(y)].index.isocalendar().week
        ).sort_index().plot(
            figsize=(10, 4),
            xlabel="Week",
            ylabel="Grass growth [kg DM ha⁻¹ day⁻¹]",
            cmap=mcolors.ListedColormap(colors),
        )
        plt.title(f"PastureBase Ireland grass growth data for {y}")
        plt.legend(ncol=6)
        plt.tight_layout()
        plt.show()

counties = list(grass_ts)

# pivot table for plotting
grass_piv = grass_ts.copy()
grass_piv["year"] = grass_piv.index.year
grass_piv["weekno"] = grass_piv.index.isocalendar().week
grass_piv = pd.pivot_table(grass_piv, index="weekno", columns="year")

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

grass_out = grass_ts.copy()
for col in counties:
    grass_out[[col]] = grass_out[[col]].replace(
        list(boxplot_stats(grass_out[[col]].dropna())[0]["fliers"]), np.nan
    )

grass_out.plot.box(
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
# plt.savefig(os.path.join("data", "grass_growth", "pasturebase", "boxplot.png"))
plt.show()

grass_out.diff().hist(figsize=(15, 18), bins=50, grid=False)
plt.tight_layout()
# plt.savefig(os.path.join("data", "grass_growth", "pasturebase", "diff_hist.png"))
plt.show()

# ## Filtering outliers using 3-week moving average

grass_out = grass_ts.reset_index()

for county in counties:
    mn = grass_out.rolling(3, center=True, on="time")[county].mean()
    grass_out[f"{county}_outlier"] = grass_out[county].sub(mn).abs().gt(10)
    grass_out[f"{county}_mn"] = mn

grass_out.set_index("time", inplace=True)

for county in counties:
    axs = grass_out.plot(
        # ylim=[0.0, 200.0],
        figsize=(10, 4),
        y=county,
        label="growth",
    )
    grass_out.plot(
        figsize=(10, 4),
        y=f"{county}_mn",
        ax=axs,
        label="moving_avg",
        color="orange",
        zorder=1,
    )
    if True in list(grass_out[f"{county}_outlier"].unique()):
        grass_out[grass_out[f"{county}_outlier"] == True].plot(
            ax=axs,
            linewidth=0.0,
            marker="*",
            y=county,
            label="outlier",
            color="crimson",
        )
    plt.title(f"PastureBase Ireland grass growth data for Co. {county}")
    plt.xlabel("")
    plt.tight_layout()
    plt.show()

for county in counties:
    axs = grass_out.loc["2017":"2019"].plot(
        ylim=[0.0, 150.0], figsize=(12, 8), y=county, label="growth"
    )
    grass_out.loc["2017":"2019"].plot(
        figsize=(10, 4),
        y=f"{county}_mn",
        ax=axs,
        label="moving_avg",
        color="orange",
        zorder=1,
    )
    if True in list(
        grass_out[f"{county}_outlier"].loc["2017":"2019"].unique()
    ):
        grass_out[grass_out[f"{county}_outlier"] == True].loc[
            "2017":"2019"
        ].plot(
            ax=axs,
            linewidth=0.0,
            marker="*",
            y=county,
            label="outlier",
            color="crimson",
        )
    plt.title(f"PastureBase Ireland grass growth data for Co. {county}")
    plt.xlabel("")
    plt.tight_layout()
    plt.show()

# with outliers
grass_out[[f"{county}_mn" for county in counties]].plot.box(
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
# plt.savefig(os.path.join("data", "grass_growth", "pasturebase", "boxplot_outliers.png"))
plt.show()
