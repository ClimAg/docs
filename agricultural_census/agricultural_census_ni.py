#!/usr/bin/env python
# coding: utf-8

# # Census of Agriculture - Northern Ireland

import os
from datetime import datetime, timezone
import pandas as pd
import pooch

URL = (
    "https://admin.opendatani.gov.uk/dataset/"
    "2a936744-dd04-457d-99b5-0000450af4fb/resource/"
    "7c3fa1e0-fadf-4cd3-b3d4-7d500274f226/download/"
    "farm-census---ward2014-2015-19-sup.csv"
)
KNOWN_HASH = None
FILE_NAME = "farm-census-ward2014.csv"
SUB_DIR = os.path.join("data", "agricultural_census", "DAERA")
DATA_FILE = os.path.join(SUB_DIR, FILE_NAME)
os.makedirs(SUB_DIR, exist_ok=True)

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

coa = pd.read_csv(DATA_FILE, encoding_errors="replace")

coa.head()

# filter grass, cattle, and sheep data
coa = coa[
    [
        "Ward2014 Code",
        "Ward2014 Name",
        "Year",
        "Total grass & rough grazing in hectares  ",
        "Total number of cattle  ",
        "Total number of sheep  ",
    ]
]

coa.head()

# keep data for 2018
coa = coa[coa["Year"] == 2018]

# rename columns
coa.rename(
    columns={
        "Ward2014 Code": "ward_2014_code",
        "Ward2014 Name": "ward_2014_name",
        "Year": "year",
        "Total grass & rough grazing in hectares  ": "total_grass_hectares",
        "Total number of cattle  ": "total_cattle",
        "Total number of sheep  ": "total_sheep",
    },
    inplace=True,
)

coa.head()

# check for missing data
coa.index[coa.isnull().any(axis=1)]

# save as a CSV file
coa.to_csv(os.path.join(SUB_DIR, "daera_agricultural_census.csv"), index=False)

