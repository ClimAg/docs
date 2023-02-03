# %%
import os
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

# %% [markdown]
# ## ROI data

# %%
bound_ie = gpd.read_file(
    os.path.join(
        "data", "boundaries", "OSi", "osi_national_statutory_boundaries.gpkg"
    ),
    layer="electoral-divisions-2019"
)

# %%
bound_ie.head()

# %%
bound_ie.shape

# %%
coa_ie = pd.read_csv(
    os.path.join("data", "agricultural_census", "CSO", "COA_2020.csv")
)

# %%
coa_ie.head()

# %%
coa_ie.shape

# %%
bound_ie["C03904V04656"] = (
    bound_ie["GUID"].replace("-", "", regex=True).str.upper()
)

# %%
bound_ie.head()

# %%
coa_ie

# %%
bound_ie

# %%
data_ie = pd.merge(bound_ie, coa_ie, on=["C03904V04656"])

# %%
data_ie.head()

# %%
data_ie.shape

# %%
base = data_ie.plot(
    column="total_cattle", figsize=(9, 9), cmap="Spectral_r", legend=True,
    scheme="equal_interval", legend_kwds={
        "loc": "upper left", "fmt": "{:.0f}", "title": "Total cattle"
    }
)
data_ie.boundary.plot(ax=base, color="darkslategrey", linewidth=.2)
plt.ticklabel_format(style="scientific", scilimits=[-4, 4])
plt.show()

# %%
base = data_ie.plot(
    column="total_sheep", figsize=(9, 9), cmap="Spectral_r", legend=True,
    scheme="equal_interval", legend_kwds={
        "loc": "upper left", "fmt": "{:.0f}", "title": "Total sheep"
    }
)
data_ie.boundary.plot(ax=base, color="darkslategrey", linewidth=.2)
plt.ticklabel_format(style="scientific", scilimits=[-4, 4])
plt.show()

# %%
base = data_ie.plot(
    column="all_grassland_hectares", figsize=(9, 9), cmap="Spectral_r",
    legend=True, scheme="equal_interval", legend_kwds={
        "loc": "upper left", "fmt": "{:.0f}",
        "title": "Total grassland (hectares)"
    }
)
data_ie.boundary.plot(ax=base, color="darkslategrey", linewidth=.2)
plt.ticklabel_format(style="scientific", scilimits=[-4, 4])
plt.show()

# %% [markdown]
# ## NI data

# %%
bound_ni = gpd.read_file(
    os.path.join("data", "boundaries", "ONS", "ons_geography.gpkg"),
    layer="ni_wards_12_2022_2157"
)

# %%
bound_ni.head()

# %%
bound_ni.shape

# %%
coa_ni = pd.read_csv(
    os.path.join(
        "data", "agricultural_census", "DAERA",
        "daera_agricultural_census.csv"
    )
)

# %%
coa_ni.head()

# %%
coa_ni.shape

# %%
coa_ni.rename(columns={"ward_2014_code": "WD22CD"}, inplace=True)

# %%
data_ni = pd.merge(bound_ni, coa_ni, on=["WD22CD"])

# %%
data_ni.head()

# %%
data_ni.shape

# %%
base = data_ni.plot(
    column="total_cattle", figsize=(9, 9), cmap="Spectral_r", legend=True,
    scheme="equal_interval", legend_kwds={
        "loc": "upper left", "fmt": "{:.0f}", "title": "Total cattle"
    }
)
data_ni.boundary.plot(ax=base, color="darkslategrey", linewidth=.2)
plt.ticklabel_format(style="scientific", scilimits=[-4, 4])
plt.show()

# %%
base = data_ni.plot(
    column="total_sheep", figsize=(9, 9), cmap="Spectral_r", legend=True,
    scheme="equal_interval", legend_kwds={
        "loc": "upper left", "fmt": "{:.0f}", "title": "Total sheep"
    }
)
data_ni.boundary.plot(ax=base, color="darkslategrey", linewidth=.2)
plt.ticklabel_format(style="scientific", scilimits=[-4, 4])
plt.show()

# %%
base = data_ni.plot(
    column="total_grass_hectares", figsize=(9, 9), cmap="Spectral_r",
    legend=True, scheme="equal_interval", legend_kwds={
        "loc": "upper left", "fmt": "{:.0f}",
        "title": "Total grassland (hectares)"
    }
)
data_ni.boundary.plot(ax=base, color="darkslategrey", linewidth=.2)
plt.ticklabel_format(style="scientific", scilimits=[-4, 4])
plt.show()
