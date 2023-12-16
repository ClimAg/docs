#!/usr/bin/env python
# coding: utf-8

# # Agricultural Census data for the Island of Ireland

import os

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# ## ROI data

bound_ie = gpd.read_file(
    os.path.join("data", "boundaries", "boundaries_all.gpkg"),
    layer="OSi_IE_electoral_divisions_2019",
)

bound_ie.head()

bound_ie.shape

coa_ie = pd.read_csv(
    os.path.join("data", "agricultural_census", "CSO", "COA_2020.csv")
)

coa_ie.head()

coa_ie.shape

bound_ie["C03904V04656"] = (
    bound_ie["GUID"].replace("-", "", regex=True).str.upper()
)

bound_ie.head()

# merge boundaries and census data
data_ie = pd.merge(bound_ie, coa_ie, on="C03904V04656", how="outer")

data_ie.shape

# find data rows without a geometry
data_na = data_ie[data_ie["geometry"].isnull()][
    [
        "C03904V04656",
        "electoral_division",
        "total_cattle",
        "total_sheep",
        "total_grass_hectares",
    ]
]

data_na

data_na.shape

# manual merging
data_na_left = data_na.copy()
data_na_right = data_na.copy()

data_na_left["ENGLISH"] = data_na_left["electoral_division"].str.split(
    expand=True, pat=" / "
)[0]

data_na_left["COUNTY"] = (
    data_na_left["electoral_division"]
    .str.split(expand=True, pat=" / ")[1]
    .str.split(expand=True, pat=",")[1]
    .str.split(expand=True, pat=" Co.")
)[1]

data_na_left.head()

data_na_right["ENGLISH"] = (
    data_na_right["electoral_division"]
    .str.split(expand=True, pat="/")[1]
    .str.split(expand=True, pat=", ")[0]
)

data_na_right["COUNTY"] = (
    data_na_right["electoral_division"]
    .str.split(expand=True, pat=" / ")[1]
    .str.split(expand=True, pat=",")[1]
    .str.split(expand=True, pat=" Co.")
)[1]

data_na_right.head()

data_na = pd.concat([data_na_left, data_na_right])

data_na.shape

# strip whitespace
data_na["ENGLISH"] = data_na["ENGLISH"].str.upper().str.strip()
data_na["COUNTY"] = data_na["COUNTY"].str.upper().str.strip()

data_na.head()

# manually change names to English
names = {
    "CEANNÚIGH": "CANUIG",
    "DOIRE IANNA": "DERRIANA",
    "AGHAVOGHILL": "AGHAVOGHIL",
    "LOUGHILL": "LOUGHIL",
    "MÁISTIR GAOITHE": "MASTERGEEHY",
}
data_na.replace({"ENGLISH": names}, inplace=True)

# drop these entries from the original dataframe
coa_ie = coa_ie[~coa_ie["C03904V04656"].isin(list(data_na["C03904V04656"]))]

coa_ie.shape

# merge boundaries and census data again
data_ie = pd.merge(bound_ie, coa_ie, on="C03904V04656", how="outer")

data_ie.shape

data_ie = pd.merge(data_ie, data_na, how="outer", on=["ENGLISH", "COUNTY"])

data_ie.head()

# finishing merges
data_ie.fillna(0, inplace=True)

data_ie["total_cattle"] = data_ie["total_cattle_x"] + data_ie["total_cattle_y"]
data_ie["total_sheep"] = data_ie["total_sheep_x"] + data_ie["total_sheep_y"]
data_ie["total_grass_hectares"] = (
    data_ie["total_grass_hectares_x"] + data_ie["total_grass_hectares_y"]
)

data_ie.replace({"electoral_division_x": {0.0: ""}}, inplace=True)
data_ie.replace({"electoral_division_y": {0.0: ""}}, inplace=True)

data_ie["electoral_division"] = data_ie["electoral_division_x"].astype(
    str
) + data_ie["electoral_division_y"].astype(str)

# drop unnecessary columns
data_ie.drop(
    columns=[
        "C03904V04656_x",
        "electoral_division_x",
        "total_cattle_x",
        "total_sheep_x",
        "total_grass_hectares_x",
        "C03904V04656_y",
        "electoral_division_y",
        "total_cattle_y",
        "total_sheep_y",
        "total_grass_hectares_y",
    ],
    inplace=True,
)

data_ie.head()

data_ie.shape

fig, axs = plt.subplots(1, 3, figsize=(15, 15))
cols = [
    ("total_cattle", "Total cattle"),
    ("total_sheep", "Total sheep"),
    ("total_grass_hectares", "Total grassland (hectares)"),
]
for i, ax in enumerate(axs.flat):
    data_ie.plot(
        column=cols[i][0],
        ax=ax,
        cmap="Spectral_r",
        scheme="equal_interval",
        edgecolor="darkslategrey",
        linewidth=0.2,
        legend=True,
        legend_kwds={
            "loc": "upper left",
            "fmt": "{:.0f}",
            "title": cols[i][1],
        },
    )
    # ax.ticklabel_format(style="scientific", scilimits=[-4, 4])
    ax.tick_params(labelbottom=False, labelleft=False)
    for legend_handle in ax.get_legend().legend_handles:
        legend_handle.set_markeredgewidth(0.2)
        legend_handle.set_markeredgecolor("darkslategrey")
plt.tight_layout()
plt.show()

# ## NI data

bound_ni = gpd.read_file(
    os.path.join("data", "boundaries", "boundaries_all.gpkg"),
    layer="ONS_NI_wards_12_2022_2157",
)

bound_ni.head()

bound_ni.shape

coa_ni = pd.read_csv(
    os.path.join(
        "data", "agricultural_census", "DAERA", "daera_agricultural_census.csv"
    )
)

coa_ni.head()

coa_ni.shape

coa_ni.rename(columns={"ward_2014_code": "WD22CD"}, inplace=True)

data_ni = pd.merge(bound_ni, coa_ni, on=["WD22CD"])

data_ni.head()

data_ni.shape

fig, axs = plt.subplots(1, 3, figsize=(15, 15), sharey=True)
cols = [
    ("total_cattle", "Total cattle"),
    ("total_sheep", "Total sheep"),
    ("total_grass_hectares", "Total grassland (hectares)"),
]
for i, ax in enumerate(axs.flat):
    data_ni.plot(
        column=cols[i][0],
        ax=ax,
        cmap="Spectral_r",
        scheme="equal_interval",
        edgecolor="darkslategrey",
        linewidth=0.2,
        legend=True,
        legend_kwds={
            "loc": "upper left",
            "fmt": "{:.0f}",
            "title": cols[i][1],
        },
    )
    # ax.ticklabel_format(style="scientific", scilimits=[-4, 4])
    ax.tick_params(labelbottom=False, labelleft=False)
    for legend_handle in ax.get_legend().legend_handles:
        legend_handle.set_markeredgewidth(0.2)
        legend_handle.set_markeredgecolor("darkslategrey")
plt.tight_layout()
plt.show()

# ## Merge

# subset data
data_ie = data_ie[
    [
        "ENGLISH",
        "COUNTY",
        "PROVINCE",
        "GUID",
        "total_cattle",
        "total_sheep",
        "total_grass_hectares",
        "electoral_division",
        "geometry",
    ]
]

data_ni = data_ni[
    [
        "WD22CD",
        "WD22NM",
        "ward_2014_name",
        "total_cattle",
        "total_sheep",
        "total_grass_hectares",
        "geometry",
    ]
]

data_ie[["total_cattle", "total_sheep", "total_grass_hectares"]] = data_ie[
    ["total_cattle", "total_sheep", "total_grass_hectares"]
].astype(float)
data_ni[["total_cattle", "total_sheep", "total_grass_hectares"]] = data_ni[
    ["total_cattle", "total_sheep", "total_grass_hectares"]
].astype(float)

data_ni["ENGLISH"] = data_ni["WD22NM"].str.upper()
data_ni["PROVINCE"] = "Ulster"

data = pd.merge(data_ie, data_ni, how="outer")

fig, axs = plt.subplots(1, 3, figsize=(15, 15), sharey=True)
cols = [
    ("total_cattle", "Total cattle"),
    ("total_sheep", "Total sheep"),
    ("total_grass_hectares", "Total grassland (hectares)"),
]
for i, ax in enumerate(axs.flat):
    data.plot(
        column=cols[i][0],
        ax=ax,
        cmap="Spectral_r",
        scheme="equal_interval",
        edgecolor="darkslategrey",
        linewidth=0.2,
        legend=True,
        legend_kwds={
            "loc": "upper left",
            "fmt": "{:.0f}",
            "title": cols[i][1],
        },
    )
    # ax.ticklabel_format(style="scientific", scilimits=[-4, 4])
    ax.tick_params(labelbottom=False, labelleft=False)
    for legend_handle in ax.get_legend().legend_handles:
        legend_handle.set_markeredgewidth(0.2)
        legend_handle.set_markeredgecolor("darkslategrey")
plt.tight_layout()
plt.show()

# ## Stocking rate

data.loc[data["total_grass_hectares"] == 0.0, "stocking_rate"] = 0.0
data.loc[data["total_grass_hectares"] > 0.0, "stocking_rate"] = (
    data["total_cattle"] * 0.8 + data["total_sheep"] * 0.1
) / data["total_grass_hectares"]

data["stocking_rate"].max()

data["stocking_rate"].min()

axs = data.plot(
    column="stocking_rate",
    cmap="Spectral_r",
    scheme="equal_interval",
    edgecolor="darkslategrey",
    linewidth=0.2,
    figsize=(7.5, 7.5),
    legend=True,
    legend_kwds={
        "loc": "upper left",
        "fmt": "{:.2f}",
        "title": "Stocking rate",
    },
)
plt.ticklabel_format(style="scientific", scilimits=[-4, 4])
for legend_handle in axs.get_legend().legend_handles:
    legend_handle.set_markeredgewidth(0.2)
    legend_handle.set_markeredgecolor("darkslategrey")
axs.tick_params(labelbottom=False, labelleft=False)
plt.tight_layout()
plt.show()

data.to_file(
    os.path.join("data", "agricultural_census", "agricultural_census.gpkg"),
    layer="stocking_rate",
)
