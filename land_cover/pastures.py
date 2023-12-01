#!/usr/bin/env python
# coding: utf-8

# # Vector layer to mask out non-pasture areas

import os
import geopandas as gpd
import matplotlib.pyplot as plt

# vectorised layer of pastures based on CLC 2018 data
pastures = gpd.read_file(
    os.path.join("data", "land-cover", "clc-2018", "clc-2018-pasture.gpkg"),
    layer="dissolved",
)
pastures.to_crs(2157, inplace=True)

# Ireland boundary
ie = gpd.read_file(
    os.path.join("data", "boundaries", "boundaries.gpkg"),
    layer="NUTS_RG_01M_2021_2157_IE",
)

# non-pasture area mask
ie_ = ie.overlay(pastures, how="symmetric_difference")

ie_.plot()
plt.tick_params(labelbottom=False, labelleft=False)
plt.tight_layout()
plt.show()

ie_.to_file(
    os.path.join("data", "boundaries", "boundaries.gpkg"),
    layer="CLC_2018_MASK_PASTURE_2157_IE",
)
