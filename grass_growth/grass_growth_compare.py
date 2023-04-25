#!/usr/bin/env python
# coding: utf-8

# # Compare grass growth time series using MERA for each county at a weekly frequency

import os
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rioxarray as rxr
import seaborn as sns
import xarray as xr
from geocube.api.core import make_geocube
from rasterstats import zonal_stats
from shapely.geometry import Polygon
import climag.plot_configs as cplt
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm

df1 = pd.read_csv(
    os.path.join(
        "data", "grass_growth", "pasturebase", "pasturebase_cleaned.csv"
    )
)
df2 = pd.read_csv(
    os.path.join(
        "data", "grass_growth", "grasscheck", "grasscheck_cleaned.csv"
    )
)
df = pd.concat([df1, df2])
df_p = pd.pivot_table(
    df[["time", "county", "value"]],
    values="value",
    index=["time"],
    columns=["county"],
)
df_p.index = pd.to_datetime(df_p.index)

mera = pd.read_csv(
    os.path.join("data", "ModVege", "growth", "MERA_growth_week_all.csv")
)
mera.rename(columns={"COUNTY": "county", "mean": "value"}, inplace=True)
mera["county"] = mera["county"].str.title()
mera_p = pd.pivot_table(
    mera, values="value", index=["time"], columns=["county"]
)
mera_p.index = pd.to_datetime(mera_p.index)

counties = list(df_p)

df["data"] = "Measured"
mera["data"] = "Simulated"
data_all = pd.concat([df, mera])
data_all.set_index("time", inplace=True)
data_all.index = pd.to_datetime(data_all.index)
# data_all_p = pd.pivot_table(
#     data_all[["county", "value", "data"]],
#     values="value", index=["time"], columns=["county", "data"]
# )
# data_all_p.resample("Y").mean()

# ## Weekly time series plots

for county in counties:
    fig = mera_p["2012":"2019"][county].plot(
        figsize=(12, 4), label="Simulated", color="darkgrey", alpha=0.75
    )
    df_p[county].plot(ax=fig.axes, label="Measured", linewidth=1)
    plt.legend(title=None)
    plt.xlabel("")
    plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
    plt.title(county)
    plt.tight_layout()
    plt.show()

# ## Stats


def get_plot_data(data_m, data_s, county, season=None):
    plot_data = pd.merge(
        data_m[[county]].rename(columns={county: "Measured"}),
        data_s[[county]].rename(columns={county: "Simulated"}),
        left_index=True,
        right_index=True,
    ).dropna()
    if season == "MAM":
        plot_data = plot_data[
            (plot_data.index.month == 3)
            | (plot_data.index.month == 4)
            | (plot_data.index.month == 5)
        ]
    elif season == "JJA":
        plot_data = plot_data[
            (plot_data.index.month == 6)
            | (plot_data.index.month == 7)
            | (plot_data.index.month == 8)
        ]
    elif season == "MarOct":
        plot_data = plot_data[
            (plot_data.index.month != 1)
            & (plot_data.index.month != 2)
            & (plot_data.index.month != 11)
            & (plot_data.index.month != 12)
        ]

    return plot_data


def rmse_by_county(data_m, data_s, counties=counties, season=None):
    rmse = pd.DataFrame(columns=["County", "RMSE"])
    for i, county in enumerate(counties):
        plot_data = get_plot_data(data_m, data_s, county, season)
        rmse.loc[i] = [
            county,
            mean_squared_error(
                plot_data["Measured"], plot_data["Simulated"], squared=False
            ),
        ]
    rmse.sort_values(by=["RMSE"], inplace=True)
    return rmse


def get_linear_regression(data_m, data_s, counties=counties, season=None):
    for county in counties:
        plot_data = get_plot_data(data_m, data_s, county, season)

        x = plot_data["Measured"]
        y = plot_data["Simulated"]

        model = sm.OLS(y, sm.add_constant(x))
        results = model.fit()
        print(county)
        print(results.summary())

        fig = plot_data.plot.scatter(x="Measured", y="Simulated", marker="x")
        b, m = results.params
        plt.axline(
            xy1=(0, b),
            slope=m,
            label=f"$y = {m:.2f}x {b:+.2f}$",
            color="crimson",
            linestyle="dotted",
        )
        plt.legend()
        plt.tight_layout()
        plt.show()


# ### MAM

# #### RMSE

rmse_by_county(df_p, mera_p, season="MAM")

# #### Linear regression

get_linear_regression(df_p, mera_p, counties=["Wexford"], season="MAM")

# ### JJA

# #### RMSE

rmse_by_county(df_p, mera_p, season="JJA")

# #### Linear regression

get_linear_regression(df_p, mera_p, counties=["Wexford"], season="JJA")

# ### All

# #### RMSE

rmse_by_county(df_p, mera_p)

# #### Linear regression

get_linear_regression(df_p, mera_p, counties=["Wexford"])

# ## Box plots - MAM growth grouped by year

for county in ["Wexford"]:
    plot_data = data_all[(data_all["county"] == county)]
    # remove Jan, Feb, Nov, Dec data
    plot_data = plot_data[
        (plot_data.index.month == 3)
        | (plot_data.index.month == 4)
        | (plot_data.index.month == 5)
    ]
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.boxplot(
        x=plot_data.index.year,
        y=plot_data["value"],
        hue=plot_data["data"],
        ax=ax,
        palette="rainbow",
    )
    plt.xlabel("")
    ax.tick_params(axis="x", rotation=90)
    plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
    plt.title(county)
    plt.legend(title=None)
    plt.tight_layout()
    plt.show()

# ## Box plots - JJA growth grouped by year

for county in ["Wexford"]:
    plot_data = data_all[(data_all["county"] == county)]
    # remove Jan, Feb, Nov, Dec data
    plot_data = plot_data[
        (plot_data.index.month == 6)
        | (plot_data.index.month == 7)
        | (plot_data.index.month == 8)
    ]
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.boxplot(
        x=plot_data.index.year,
        y=plot_data["value"],
        hue=plot_data["data"],
        ax=ax,
        palette="rainbow",
    )
    plt.xlabel("")
    ax.tick_params(axis="x", rotation=90)
    plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
    plt.title(county)
    plt.legend(title=None)
    plt.tight_layout()
    plt.show()

# ## Box plots - March - October growth grouped by year

for county in ["Wexford"]:
    plot_data = data_all[(data_all["county"] == county)]
    # remove Jan, Feb, Nov, Dec data
    plot_data = plot_data[
        (plot_data.index.month != 1)
        & (plot_data.index.month != 2)
        & (plot_data.index.month != 11)
        & (plot_data.index.month != 12)
    ]
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.boxplot(
        x=plot_data.index.year,
        y=plot_data["value"],
        hue=plot_data["data"],
        ax=ax,
        palette="rainbow",
    )
    plt.xlabel("")
    ax.tick_params(axis="x", rotation=90)
    plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
    plt.title(county)
    plt.legend(title=None)
    plt.tight_layout()
    plt.show()
