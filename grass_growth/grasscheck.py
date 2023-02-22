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
# vol. 25, pp. 716–718. [Online]. Available at
# <https://www.europeangrassland.org/fileadmin/documents/Infos/Printed_Matter/Proceedings/EGF2020.pdf>
# (Accessed 13 September 2022).

import os
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import pandas as pd

print("Last updated:", datetime.now(tz=timezone.utc))

DATA_DIR = os.path.join("data", "grass-growth", "grasscheck", "grasscheck.ods")

grass_ni = pd.read_excel(DATA_DIR, parse_dates=["week"])

grass_ni.head()

grass_ni.shape

# use weekly time series starting on Monday to fill missing rows
grass_ts = pd.DataFrame(
    pd.date_range(
        str(grass_ni["week"][0].year) + "-01-01",
        str(grass_ni["week"][len(grass_ni) - 1].year) + "-12-31",
        freq="W-MON",
    ),
    columns=["week"],
)

grass_ts = pd.merge(grass_ts, grass_ni, how="outer")

grass_ts.head()

grass_ts.shape

DATA_DIR = os.path.join("data", "grass-growth", "grasscheck", "grasscheck.csv")

# save time series
grass_ts.to_csv(DATA_DIR, index=False)

# set timestamps as the index
grass_ts.index = grass_ts["week"]

grass_ts.drop(columns=["week"], inplace=True)

# capitalise county names
counties = []
for c in list(grass_ts):
    counties.append(c.capitalize())

grass_ts.columns = counties

grass_ts.plot(figsize=(12, 4), linewidth=1, cmap="viridis")
plt.title("Grass growth in Northern Ireland [Data: GrassCheck NI]")
plt.xlabel("")
plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
plt.show()

for c in counties:
    grass_ts[c].plot(figsize=(12, 4), linewidth=1)
    plt.title(f"Grass growth in Co. {c} [Data: GrassCheck NI]")
    plt.xlabel("")
    plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
    plt.show()

years = list(grass_ts.index.year.unique())
for y in years:
    grass_ts.loc[str(y)].plot(figsize=(12, 4), linewidth=1.25, cmap="viridis")
    plt.title(f"Grass growth in Northern Ireland in {y} [Data: GrassCheck NI]")
    plt.xlabel("")
    plt.ylabel("Grass growth [kg DM ha⁻¹ day⁻¹]")
    plt.show()
