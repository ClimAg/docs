#!/usr/bin/env python
# coding: utf-8

# # Compare grass growth time series using MERA for each county at a weekly frequency

import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error

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
    os.path.join("data", "ModVege", "growth", "MERA_growth_week_pasture.csv")
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

# ## Number of data points

ax = (
    pd.DataFrame(df_p.count())
    .sort_values(by=0)
    .plot.bar(
        legend=False,
        figsize=(12, 5),
        color="lightskyblue",
        edgecolor="darkslategrey",
    )
)
ax.bar_label(ax.containers[0], padding=2)
plt.xlabel("")
plt.ylabel("Number of data points")
plt.tight_layout()
plt.show()

# ## Averages

lta_all = pd.DataFrame(df_p.mean(), columns=["All seasons"]).sort_values(
    by="All seasons"
)

lta_mam = pd.DataFrame(
    df_p[
        (df_p.index.month == 3)
        | (df_p.index.month == 4)
        | (df_p.index.month == 5)
    ].mean(),
    columns=["MAM"],
).sort_values(by="MAM")

lta_jja = pd.DataFrame(
    df_p[
        (df_p.index.month == 6)
        | (df_p.index.month == 7)
        | (df_p.index.month == 8)
    ].mean(),
    columns=["JJA"],
).sort_values(by="JJA")

lta_son = pd.DataFrame(
    df_p[
        (df_p.index.month == 9)
        | (df_p.index.month == 10)
        | (df_p.index.month == 11)
    ].mean(),
    columns=["SON"],
).sort_values(by="SON")

pd.concat([lta_mam, lta_jja, lta_son, lta_all], axis=1).sort_values(
    by=["All seasons", "SON", "JJA", "MAM"]
).plot.bar(
    figsize=(14, 5),
    edgecolor="darkslategrey",
    color=["lightskyblue", "mediumvioletred", "gold", "slategrey"],
)
plt.xlabel("")
plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
plt.tight_layout()
plt.show()

pd.concat([lta_mam, lta_jja, lta_son, lta_all], axis=1).to_csv(
    os.path.join("data", "grass_growth", "average_growth.csv")
)

# ### 2018 averages

a2018_all = pd.DataFrame(
    df_p.loc["2018"].mean(), columns=["2018"]
).sort_values(by="2018")

a2018_mam = pd.DataFrame(
    df_p[
        (df_p.index.month == 3)
        | (df_p.index.month == 4)
        | (df_p.index.month == 5)
    ]
    .loc["2018"]
    .mean(),
    columns=["2018 (MAM)"],
).sort_values(by="2018 (MAM)")

a2018_jja = pd.DataFrame(
    df_p[
        (df_p.index.month == 6)
        | (df_p.index.month == 7)
        | (df_p.index.month == 8)
    ]
    .loc["2018"]
    .mean(),
    columns=["2018 (JJA)"],
).sort_values(by="2018 (JJA)")

a2018_son = pd.DataFrame(
    df_p[
        (df_p.index.month == 9)
        | (df_p.index.month == 10)
        | (df_p.index.month == 11)
    ]
    .loc["2018"]
    .mean(),
    columns=["2018 (SON)"],
).sort_values(by="2018 (SON)")

pd.concat([a2018_mam, a2018_jja, a2018_son, a2018_all], axis=1).sort_values(
    by=["2018", "2018 (SON)", "2018 (JJA)", "2018 (MAM)"]
).plot.bar(
    figsize=(14, 5),
    edgecolor="darkslategrey",
    color=["lightskyblue", "mediumvioletred", "gold", "slategrey"],
)
plt.xlabel("")
plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
plt.tight_layout()
plt.show()

pd.concat([a2018_mam, a2018_jja, a2018_son, a2018_all], axis=1).to_csv(
    os.path.join("data", "grass_growth", "average_growth_2018.csv")
)

# ## Weekly time series plots

for county in counties:
    plt.axhline(
        y=float(lta_all.loc[county]),
        linestyle="dashed",
        color="darkslategrey",
        alpha=0.75,  # label="Average (measured)"
    )
    # plt.axhline(
    #     y=float(lta_mam.loc[county]), linestyle="dotted",
    #     label="Average (MAM)", color="darkslategrey", alpha=.75
    # )
    # plt.axhline(
    #     y=float(lta_jja.loc[county]), linestyle="dashed",
    #     label="Average (JJA)", color="darkslategrey", alpha=.75
    # )
    # plt.axhline(
    #     y=float(lta_son.loc[county]), linestyle="dashdot",
    #     label="Average (SON)", color="darkslategrey", alpha=.75
    # )
    fig = mera_p["2012":"2019"][county].plot(
        figsize=(12, 4), label="Simulated", color="lightskyblue"
    )
    df_p[county].plot(
        ax=fig.axes, label="Measured", color="crimson", alpha=0.75
    )
    plt.legend(title=None, ncols=2, loc="upper right")
    plt.xlabel("")
    plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
    # plt.title(county)
    plt.tight_layout()
    print(county)
    plt.show()

# ## Stats


def get_plot_data(data_m, data_s, county, season=None):
    if county is None:
        plot_data = (
            pd.merge(
                data_m.melt(ignore_index=False)
                .reset_index()
                .set_index(["time", "county"])
                .rename(columns={"value": "Measured"}),
                data_s.melt(ignore_index=False)
                .reset_index()
                .set_index(["time", "county"])
                .rename(columns={"value": "Simulated"}),
                left_index=True,
                right_index=True,
            )
            .dropna()
            .reset_index()
            .set_index("time")
        )
    else:
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
    elif season == "SON":
        plot_data = plot_data[
            (plot_data.index.month == 9)
            | (plot_data.index.month == 10)
            | (plot_data.index.month == 11)
        ]

    return plot_data


def rmse_by_county(data_m, data_s, counties=counties, season=None):
    if season:
        col_name = season
    else:
        col_name = "All seasons"
    rmse = pd.DataFrame(columns=["County", col_name])
    for i, county in enumerate(counties):
        plot_data = get_plot_data(data_m, data_s, county, season)
        rmse.loc[i] = [
            county,
            mean_squared_error(
                plot_data["Measured"], plot_data["Simulated"], squared=False
            ),
        ]
    plot_data = get_plot_data(data_m, data_s, county=None, season=season)
    rmse.loc[i] = [
        "All counties",
        mean_squared_error(
            plot_data["Measured"], plot_data["Simulated"], squared=False
        ),
    ]
    # rmse.sort_values(by=[col_name], inplace=True)
    return rmse


def rmse_all(data_m, data_s):
    plot_data = pd.merge(
        pd.merge(
            pd.merge(
                rmse_by_county(df_p, mera_p, season="MAM"),
                rmse_by_county(df_p, mera_p, season="JJA"),
                on="County",
            ),
            rmse_by_county(df_p, mera_p, season="SON"),
            on="County",
        ),
        rmse_by_county(df_p, mera_p, season=None),
        on="County",
    )
    plot_data.sort_values(by="All seasons", inplace=True)
    return plot_data


def get_linear_regression(data_m, data_s, county, season=None):
    plot_data = get_plot_data(data_m, data_s, county, season)
    if county:
        print(county)

    x = plot_data["Measured"]
    y = plot_data["Simulated"]

    model = sm.OLS(y, sm.add_constant(x))
    results = model.fit()

    print(results.summary())

    # fig = plot_data.plot.scatter(
    #     x="Measured", y="Simulated", marker="x", color="dodgerblue"
    # )
    fig = sns.jointplot(
        x="Measured",
        y="Simulated",
        data=plot_data,
        color="lightskyblue",
        marginal_kws=dict(bins=25),
    )
    # x = y line
    plt.axline(
        (0, 0),
        slope=1,
        color="mediumvioletred",
        linestyle="dotted",
        linewidth=2,
    )
    b, m = results.params
    r = results.rsquared
    plt.axline(
        (0, b),
        slope=m,
        label=f"$y = {m:.2f}x {b:+.2f}$\n$R^2 = {r:.2f}$",
        color="crimson",
        linewidth=2,
    )
    plt.xlim([-5, 155])
    plt.ylim([-5, 155])
    plt.legend(loc="upper left")
    # plt.axis("equal")
    plt.xlabel("Measured [kg DM ha⁻¹ day⁻¹]")
    plt.ylabel("Simulated [kg DM ha⁻¹ day⁻¹]")
    plt.tight_layout()
    plt.show()


# ### RMSE

rmse_all(df_p, mera_p)

rmse_all(df_p, mera_p).plot.bar(
    figsize=(14, 5),
    x="County",
    edgecolor="darkslategrey",
    color=["lightskyblue", "mediumvioletred", "gold", "slategrey"],
)
plt.xlabel("")
plt.ylabel("Root-mean-square error")
plt.tight_layout()
plt.show()

# ### Linear regression - all counties

# #### MAM

get_linear_regression(df_p, mera_p, county=None, season="MAM")

# #### JJA

get_linear_regression(df_p, mera_p, county=None, season="JJA")

# #### SON

get_linear_regression(df_p, mera_p, county=None, season="SON")

# #### All seasons

get_linear_regression(df_p, mera_p, county=None)

# ## Box plots


def box_plots(counties, season):
    for county in counties:
        plot_data = data_all[(data_all["county"] == county)]
        # keep season data
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
        fig, ax = plt.subplots(figsize=(15, 5))
        sns.boxplot(
            x=plot_data.index.year,
            y=plot_data["value"],
            hue=plot_data["data"],
            ax=ax,
            palette="Pastel1",
            showmeans=True,
            meanprops={
                "markeredgecolor": "darkslategrey",
                "marker": "d",
                "markerfacecolor": (1, 1, 0, 0),
                "markersize": 4.5,
            },
            flierprops={
                "marker": "o",
                "markerfacecolor": (1, 1, 0, 0),
                "markeredgecolor": "darkslategrey",
            },
            boxprops={"edgecolor": "darkslategrey", "alpha": 0.75},
            whiskerprops={"color": "darkslategrey", "alpha": 0.75},
            capprops={"color": "darkslategrey", "alpha": 0.75},
            medianprops={"color": "darkslategrey", "alpha": 0.75},
        )
        plt.xlabel("")
        ax.tick_params(axis="x", rotation=90)
        plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
        # plt.title(county)
        plt.legend(title=None)
        plt.tight_layout()
        print(county)
        plt.show()


# ### MAM growth grouped by year

box_plots(["Wexford"], "MAM")

# ### JJA growth grouped by year

box_plots(["Wexford"], "JJA")
