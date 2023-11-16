#!/usr/bin/env python
# coding: utf-8

# # Grass10
#
# Data taken from Teagasc Grass10 newsletters
# <https://www.teagasc.ie/crops/grassland/grass10/>

import os
from datetime import datetime, timezone

import matplotlib.pyplot as plt
import pandas as pd

print("Last updated:", datetime.now(tz=timezone.utc))

DATA_DIR = os.path.join("data", "grass-growth", "grass10", "grass10.ods")

grass = pd.read_excel(DATA_DIR, parse_dates=["week"])

grass.head()

grass.shape

# use weekly time series starting on Monday to fill missing rows
grass_ts = pd.DataFrame(
    pd.date_range(
        str(grass["week"][0].year) + "-01-01",
        str(grass["week"][len(grass) - 1].year) + "-12-31",
        freq="W-MON",
    ),
    columns=["week"],
)

grass_ts = pd.merge(grass_ts, grass, how="outer")

grass_ts.head()

grass_ts.shape

list(grass_ts)

DATA_DIR = os.path.join("data", "grass-growth", "grass10", "grass10.csv")

# save time series
grass_ts.to_csv(DATA_DIR, index=False)

ax = grass_ts.plot(
    "week",
    "growth_dairy",
    figsize=(12, 4),
    ylabel="Growth or demand [kg DM ha⁻¹]",
    label="Growth",
)
grass_ts.plot("week", "demand_dairy", ax=ax, label="Demand")
grass_ts.plot(
    "week",
    "stocking_rate_dairy",
    ax=ax,
    secondary_y=True,
    ylabel="Stocking rate [LU ha⁻¹]",
    label="Stocking rate",
)
ax.set_xlabel("")
plt.show()

ax = grass_ts.plot(
    "week",
    "growth_drystock",
    figsize=(12, 4),
    ylabel="Growth or demand [kg DM ha⁻¹]",
    label="Growth",
)
grass_ts.plot("week", "demand_drystock", ax=ax, label="Demand")
grass_ts.plot(
    "week",
    "stocking_rate_drystock",
    ax=ax,
    secondary_y=True,
    ylabel="Stocking rate [LU ha⁻¹]",
    label="Stocking rate",
)
ax.set_xlabel("")
plt.show()

ax = grass_ts.plot(
    "week",
    "pregrazing_yield_dairy",
    figsize=(12, 4),
    ylabel="Pregrazing yield [kg DM ha⁻¹]",
    label="Dairy",
)
grass_ts.plot("week", "pregrazing_yield_drystock", ax=ax, label="Drystock")
ax.set_xlabel("")
plt.show()

ax = grass_ts.plot(
    "week",
    "AFC_dairy",
    figsize=(12, 4),
    ylabel="AFC [kg DM ha⁻¹]",
    label="Dairy",
)
grass_ts.plot("week", "AFC_drystock", ax=ax, label="Drystock")
ax.set_xlabel("")
plt.show()
