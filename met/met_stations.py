#!/usr/bin/env python
# coding: utf-8

# # Met stations

import os
from datetime import datetime, timezone

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pooch
from matplotlib import ticker

import climag.plot_configs as cplt

print("Last updated:", datetime.now(tz=timezone.utc))

# ## Met Éireann stations
#
# - Station details can be found here:
#   <https://cli.fusio.net/cli/climate_data/webdata/StationDetails.csv>
# - <https://www.met.ie/climate/weather-observing-stations>
# - Check the "Show closed stations" box to obtain data for this replaced
#   station: <https://www.met.ie/climate/available-data/historical-data>

URL = "https://cli.fusio.net/cli/climate_data/webdata/StationDetails.csv"
SUB_DIR = os.path.join("data", "met", "MetEireann")
KNOWN_HASH = None
os.makedirs(SUB_DIR, exist_ok=True)
FILE_NAME = "StationDetails.csv"

# download data if necessary
if not os.path.isfile(os.path.join(SUB_DIR, FILE_NAME)):
    pooch.retrieve(
        url=URL, known_hash=KNOWN_HASH, fname=FILE_NAME, path=SUB_DIR
    )

    with open(
        os.path.join(SUB_DIR, f"{FILE_NAME[:-4]}.txt"), "w", encoding="utf-8"
    ) as outfile:
        outfile.write(
            f"Data downloaded on: {datetime.now(tz=timezone.utc)}\n"
            f"Download URL: {URL}"
        )

stations_roi = pd.read_csv(os.path.join(SUB_DIR, FILE_NAME))

stations_roi.shape

stations_roi.head()

# convert coordinates to well known text
stations_roi["wkt"] = (
    "POINT ("
    + stations_roi["longitude"].astype(str)
    + " "
    + stations_roi["latitude"].astype(str)
    + ")"
)

# convert wkt to geometry
stations_roi = gpd.GeoDataFrame(
    stations_roi,
    geometry=gpd.GeoSeries.from_wkt(stations_roi["wkt"]),
    crs="EPSG:4326",
)

# drop wkt, lon, lat column
stations_roi.drop(columns=["wkt", "longitude", "latitude"], inplace=True)

# replace null values
stations_roi = stations_roi.replace(
    {"close year": {"(null)": np.nan}, "open year": {"(null)": np.nan}}
)

# stations_roi["close year"] = pd.to_numeric(stations_roi["close year"])
# stations_roi["open year"] = pd.to_numeric(stations_roi["open year"])

# # filter stations that have data for the historic reference period
# stations_roi = stations_roi[
#     (stations_roi["close year"] >= 2005) &
#     (stations_roi["open year"] <= 1976)
# ]

# # replace null values
# stations_roi = stations_roi.replace({"close year": {np.nan: None}})
# stations_roi = stations_roi.replace({"open year": {np.nan: None}})

stations_roi.head()

stations_roi.shape

# ## Met Office data for stations in Northern Ireland
#
# <https://www.metoffice.gov.uk/research/climate/maps-and-data/uk-synoptic-and-climate-stations>
#
# Met Office (2019): Met Office MIDAS Open: UK Land Surface Stations Data
# (1853-current). Centre for Environmental Data Analysis.
# <https://catalogue.ceda.ac.uk/uuid/dbd451271eb04662beade68da43546e1>

SUB_DIR = os.path.join("data", "met", "MetOffice")

stations_ni = pd.read_csv(
    os.path.join(
        SUB_DIR,
        "midas-open_uk-daily-weather-obs_dv-202107_station-metadata.csv",
    ),
    skiprows=46,
    skipfooter=1,
    engine="python",
)

stations_ni.shape

stations_ni.head()

# list of historic counties in NI
# https://en.wikipedia.org/wiki/Historic_counties_of_the_United_Kingdom
counties_ni = [
    "antrim",
    "armagh",
    "down",
    "fermanagh",
    "londonderry",
    "tyrone",
]

# keep only NI data
stations_ni = stations_ni[stations_ni["historic_county"].isin(counties_ni)]

# convert coordinates to well known text
stations_ni["wkt"] = (
    "POINT ("
    + stations_ni["station_longitude"].astype(str)
    + " "
    + stations_ni["station_latitude"].astype(str)
    + ")"
)

# convert wkt to geometry
stations_ni = gpd.GeoDataFrame(
    stations_ni,
    geometry=gpd.GeoSeries.from_wkt(stations_ni["wkt"]),
    crs="EPSG:4326",
)

# drop wkt, lon, lat column
stations_ni.drop(
    columns=["wkt", "station_longitude", "station_latitude"], inplace=True
)

# # filter stations that have data for the historic reference period
# stations_ni = stations_ni[
#     (stations_ni["last_year"] >= 2005) & (stations_ni["first_year"] <= 1976)
# ]

# rename Londonderry to Derry
stations_ni = stations_ni.replace(
    {"historic_county": {"londonderry": "derry"}}
)

stations_ni.head()

stations_ni.shape

# ## Plot

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries_all.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")

base = ie.plot(
    color="navajowhite",
    figsize=(9, 9),
    edgecolor="darkslategrey",
    linewidth=0.5,
)
stations_roi.to_crs(ie.crs).to_crs(ie.crs).plot(
    ax=base, color="royalblue", markersize=5, label="Met Éireann"
)
stations_ni.to_crs(ie.crs).plot(
    ax=base, color="crimson", markersize=5, label="Met Office"
)

# base.xaxis.set_major_formatter(cplt.longitude_tick_format)
# base.yaxis.set_major_formatter(cplt.latitude_tick_format)
# base.yaxis.set_major_locator(ticker.MultipleLocator(1))
base.tick_params(labelbottom=False, labelleft=False)

plt.title("Meteorological stations in the Island of Ireland")
plt.text(
    625000,
    500000,
    "© Met Éireann\n© Met Office, NERC EDS CEDA\n"
    + "© Ordnance Survey Ireland\n"
    "© Ordnance Survey Northern Ireland",
)
plt.legend(loc="upper left")

plt.show()

# save as GPKG
GPKG_MET = os.path.join("data", "met", "met_stations.gpkg")
stations_roi.to_file(GPKG_MET, layer="MetEireann")
stations_ni.to_file(GPKG_MET, layer="MetOffice")
