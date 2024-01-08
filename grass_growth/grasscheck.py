#!/usr/bin/env python
# coding: utf-8

# # GrassCheck NI
#
# <https://agrisearch.org/grasscheck>
#
# Huson, K. M., Lively, F. O., Aubry, A., Takahashi, T., Gordon, A. and
# McDonnell, D. A. (2020).
# 'GrassCheck: monitoring grass growth and maximizing grass utilisation on UK
# farms',
# in Virkajärvi, P. et al. (eds),
# *Meeting the future demands for grassland production*,
# Grassland Science in Europe, Helsinki, Finland, European Grassland Federation,
# vol. 25, pp. 716-718. [Online]. Available at
# <https://www.europeangrassland.org/fileadmin/documents/Infos/Printed_Matter/Proceedings/EGF2020.pdf>
# (Accessed 13 September 2022).

import os
from datetime import datetime, timezone

import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = os.path.join(
    "data", "grass_growth", "GrassCheckNI", "grasscheck.ods"
)

grass_ts = pd.read_excel(DATA_DIR, parse_dates=["week"])

# rename column
grass_ts.rename(columns={"week": "time"}, inplace=True)

grass_ts.head()

grass_ts.shape

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

grass_ts.head()

grass_ts.shape

DATA_DIR = os.path.join(
    "data", "grass_growth", "GrassCheckNI", "grasscheck.csv"
)

# save time series
grass_ts.to_csv(DATA_DIR, index=False)

# set timestamps as the index
grass_ts.set_index("time", inplace=True)

# capitalise county names
counties = []
for c in list(grass_ts):
    counties.append(c.capitalize())
grass_ts.columns = counties

grass_ts.head()

# pivot table for plotting
grass_piv = grass_ts.copy()
grass_piv["year"] = grass_piv.index.year
grass_piv["weekno"] = grass_piv.index.isocalendar().week
grass_piv = pd.pivot_table(grass_piv, index="weekno", columns="year")

grass_piv.head()

# ## Time series

for county in counties:
    grass_piv[county].plot(
        figsize=(12, 4),
        xlabel="Week",
        ylabel="Grass growth [kg DM ha⁻¹ day⁻¹]",
    )
    plt.title(f"GrassCheck NI data for Co. {county}")
    plt.legend(title=None)
    plt.tight_layout()
    plt.show()

# ## Distribution

grass_ts.plot.box(
    figsize=(4, 5),
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
plt.show()

grass_ts.diff().hist(figsize=(6, 8), bins=50, grid=False)
plt.tight_layout()
plt.show()

grass_ts_ = grass_ts.melt(ignore_index=False).rename(
    columns={"variable": "county"}
)

grass_ts_["weekno"] = grass_ts_.index.isocalendar().week

grass_ts_.reset_index(inplace=True)

DATA_DIR = os.path.join(
    "data", "grass_growth", "GrassCheckNI", "grasscheck_cleaned.csv"
)

# save time series
grass_ts_.to_csv(DATA_DIR, index=False)

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
    grass_out[grass_out[f"{county}_outlier"] == True].plot(
        ax=axs,
        linewidth=0.0,
        marker="*",
        y=county,
        label="outlier",
        color="crimson",
    )
    plt.title(county)
    plt.xlabel("")
    plt.tight_layout()
    plt.show()

for county in counties:
    axs = grass_out.loc["2017":"2019"].plot(
        # ylim=[0.0, 200.0],
        figsize=(12, 8),
        y=county,
        label="growth",
    )
    grass_out.loc["2017":"2019"].plot(
        figsize=(10, 4),
        y=f"{county}_mn",
        ax=axs,
        label="moving_avg",
        color="orange",
        zorder=1,
    )
    grass_out[grass_out[f"{county}_outlier"] == True].loc["2017":"2019"].plot(
        ax=axs,
        linewidth=0.0,
        marker="*",
        y=county,
        label="outlier",
        color="crimson",
    )
    plt.title(county)
    plt.xlabel("")
    plt.tight_layout()
    plt.show()

grass_out[[f"{county}_mn" for county in counties]].plot.box(
    figsize=(4, 5),
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
plt.show()
