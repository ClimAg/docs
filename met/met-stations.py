# %% [markdown]
# # Met stations

# %%
import os
from datetime import datetime, timezone
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from climag.download_data import download_data

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %% [markdown]
# ## Met Éireann stations
#
# - Station details can be found here:
#   <https://cli.fusio.net/cli/climate_data/webdata/StationDetails.csv>
# - <https://www.met.ie/climate/weather-observing-stations>
# - Check the "Show closed stations" box to obtain data for this replaced
#   station: <https://www.met.ie/climate/available-data/historical-data>

# %%
URL = "https://cli.fusio.net/cli/climate_data/webdata/StationDetails.csv"
SUB_DIR = os.path.join("data", "met", "meteireann", "raw")

# %%
# download data if necessary
download_data(server=URL, dl_dir=SUB_DIR)

# %%
os.listdir(SUB_DIR)

# %%
stations_roi = pd.read_csv(os.path.join(SUB_DIR, "StationDetails.csv"))

# %%
stations_roi.shape

# %%
stations_roi.head()

# %%
# convert coordinates to well known text
stations_roi["wkt"] = (
    "POINT (" + stations_roi["longitude"].astype(str) + " " +
    stations_roi["latitude"].astype(str) + ")"
)

# %%
# convert wkt to geometry
stations_roi = gpd.GeoDataFrame(
    stations_roi,
    geometry=gpd.GeoSeries.from_wkt(stations_roi["wkt"]),
    crs="EPSG:4326"
)

# %%
# drop wkt, lon, lat column
stations_roi.drop(columns=["wkt", "longitude", "latitude"], inplace=True)

# %%
stations_roi["close year"].unique()

# %%
stations_roi["open year"].unique()

# %%
# replace null values so that the data can be filtered
stations_roi = stations_roi.replace({
    "close year": {"(null)": 9999},
    "open year": {"(null)": 0}
})

# %%
stations_roi["close year"] = pd.to_numeric(stations_roi["close year"])
stations_roi["open year"] = pd.to_numeric(stations_roi["open year"])

# %%
# filter stations that have data for the historic reference period
stations_roi = stations_roi[
    (stations_roi["close year"] >= 2005) & (stations_roi["open year"] <= 1976)
]

# %%
stations_roi

# %%
# replace null values
stations_roi = stations_roi.replace({"close year": {9999: None}})
stations_roi = stations_roi.replace({"open year": {0: None}})

# %%
stations_roi.head()

# %%
stations_roi.shape

# %% [markdown]
# ## Met Office data for stations in Northern Ireland
#
# <https://www.metoffice.gov.uk/research/climate/maps-and-data/uk-synoptic-and-climate-stations>
#
# Met Office (2019): Met Office MIDAS Open: UK Land Surface Stations Data
# (1853-current). Centre for Environmental Data Analysis.
# <https://catalogue.ceda.ac.uk/uuid/dbd451271eb04662beade68da43546e1>

# %%
SUB_DIR = os.path.join("data", "met", "metoffice", "raw")

# %%
stations_ni = pd.read_csv(
    os.path.join(
        SUB_DIR,
        "midas-open_uk-daily-rain-obs_dv-202107_station-metadata.csv"
    ),
    skiprows=46,
    skipfooter=1,
    engine="python"
)

# %%
stations_ni.shape

# %%
stations_ni.head()

# %%
# list of historic counties in NI
# https://en.wikipedia.org/wiki/Historic_counties_of_the_United_Kingdom
counties_ni = [
    "antrim", "armagh", "down", "fermanagh", "londonderry", "tyrone"
]

# %%
# keep only NI data
stations_ni = stations_ni[stations_ni["historic_county"].isin(counties_ni)]

# %%
# convert coordinates to well known text
stations_ni["wkt"] = (
    "POINT (" + stations_ni["station_longitude"].astype(str) + " " +
    stations_ni["station_latitude"].astype(str) + ")"
)

# %%
# convert wkt to geometry
stations_ni = gpd.GeoDataFrame(
    stations_ni,
    geometry=gpd.GeoSeries.from_wkt(stations_ni["wkt"]),
    crs="EPSG:4326"
)

# %%
# drop wkt, lon, lat column
stations_ni.drop(
    columns=["wkt", "station_longitude", "station_latitude"],
    inplace=True
)

# %%
stations_ni["first_year"].unique()

# %%
stations_ni["last_year"].unique()

# %%
# filter stations that have data for the historic reference period
stations_ni = stations_ni[
    (stations_ni["last_year"] >= 2005) & (stations_ni["first_year"] <= 1976)
]

# %%
# rename Londonderry to Derry
stations_ni = stations_ni.replace(
    {"historic_county": {"londonderry": "derry"}}
)

# %%
stations_ni.head()

# %%
stations_ni.shape

# %% [markdown]
# ## Plot

# %%
# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_Ireland")

# %%
base = ie.plot(color="navajowhite", figsize=(9, 9))
ie.boundary.plot(ax=base, color="darkslategrey", linewidth=.4)
stations_roi.plot(
    ax=base, color="royalblue", markersize=5, label="Met Éireann"
)
stations_ni.plot(ax=base, color="crimson", markersize=5, label="Met Office")


def longitude(x, pos):
    """The two arguments are the value and tick position."""
    return "{:,.0f}°W".format(x * -1)


base.xaxis.set_major_formatter(longitude)
base.yaxis.set_major_formatter("{x}°N")

plt.title("Meteorological stations in Ireland")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
plt.text(
    -8, 51.275,
    "© Met Éireann\n© Met Office, NERC EDS CEDA\n" +
    "© Ordnance Survey Ireland\n"
    "© Ordnance Survey Northern Ireland"
)
plt.legend(loc="upper left")

plt.show()

# %%
# save as GPKG
GPKG_MET = os.path.join("data", "met", "stations.gpkg")
stations_roi.to_file(GPKG_MET, layer="meteireann")
stations_ni.to_file(GPKG_MET, layer="metoffice")
