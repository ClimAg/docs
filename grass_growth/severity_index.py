#!/usr/bin/env python
# coding: utf-8

import os

import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import mean_squared_error

data = {
    1946: np.nan,
    1947: 5,
    1948: 2,
    1950: 2,
    1955: 2,
    1956: 2,
    1958: 1,
    1962: 3,
    1963: 3,
    1974: 3,
    1975: 3,
    1976: 5,
    1985: 3,
    1986: 3,
    1987: 1,
    1995: 1,
    1998: 1,
    1999: 1,
    2001: 1,
    2002: 1,
    2007: 1,
    2008: 1,
    2009: 1,
    2012: 5,
    2013: 5,
    2018: 3,
    2020: 1,
    2022: 1,
}

data_ = pd.DataFrame(data, index=[0]).transpose().reset_index()

data_["time"] = pd.to_datetime(data_["index"], format="%Y")

data_ = data_.set_index("time").resample("Y").mean()

data_["year"] = data_.index.year

plt.figure(figsize=(12, 5))
ax = sns.barplot(data_, x="year", y=0, color="#762a83")
ax.set_xlabel("Year")
ax.set_ylabel("Severity Index")
ax.grid(which="major", axis="y")
ax.tick_params(axis="x", labelrotation=90)
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
sns.despine()
plt.tight_layout()
plt.show()
