# %% [markdown]
# # Growing season definition

# %%
import os
from datetime import datetime, timezone
import pandas as pd
import pooch
import numpy as np

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
# DATA_DRIVE = "/run/media/nms/Elements"
DATA_DRIVE = "data"

# %% [markdown]
# ## Valentia Observatory, Co. Kerry
#
# <https://data.gov.ie/dataset/valentia-observatory-daily-data>

# %%
URL = "https://cli.fusio.net/cli/climate_data/webdata/dly2275.csv"
SUB_DIR = os.path.join(DATA_DRIVE, "MetEireann")
KNOWN_HASH = "0fc478a2d8e475f965bbf05e26c1efd6fd7f33468e152ce02dc51b042a771e85"
os.makedirs(SUB_DIR, exist_ok=True)
FILE_NAME = "dly2275.csv"

# %%
pooch.retrieve(
    url=URL,
    known_hash=KNOWN_HASH,
    fname=FILE_NAME,
    path=SUB_DIR
)

# %%
val = pd.read_csv(
    os.path.join(SUB_DIR, FILE_NAME), skiprows=24, parse_dates=["date"]
)

# %%
val.head()

# %%
# keep only min and max air temps
val = val[["date", "maxtp", "mintp"]]

# %%
# filter data for 1954 - 1968
val = val[(val["date"].dt.year >= 1954) & (val["date"].dt.year <= 1968)]

# %%
val.head()

# %%
# calculate mean air temperature
val["meantp"] = val[["maxtp", "mintp"]].mean(axis=1)

# %%
# keep only mean and date columns
val = val[["date", "meantp"]]

# %%
# return only mean values above 4, and subtract by 4
val.loc[(val["meantp"] >= 4.0), "tgrowth"] = val["meantp"] - 4.0

# %%
val.head()

# %%
# extract data to determine beginning of growing season
st_1 = {}
for y in val["date"].dt.year.unique():
    st_1[y] = val[
        (val["date"] >= f"{y}-01-01") & (val["date"] <= f"{y}-01-28")
    ]

# %%
# extract data to determine end of growing season
st_2 = {}
for y in val["date"].dt.year.unique():
    if y < val["date"].dt.year.max():
        st_2[y] = val[
            (val["date"] >= f"{y}-01-01") & (val["date"] <= f"{y + 1}-01-09")
        ]

# %%
# sum of temperatures at the beginning
st_1_list = []
for y in st_1.keys():
    st_1_list.append(list(st_1[y]["tgrowth"].cumsum())[-1])
# remove NaN
st_1_list = [n for n in st_1_list if str(n) != "nan"]

# %%
# sum of temperatures at the end
st_2_list = []
for y in st_2.keys():
    st_2_list.append(list(st_2[y]["tgrowth"].cumsum())[-1])
# remove NaN
st_2_list = [n for n in st_2_list if str(n) != "nan"]

# %%
st_1_list

# %%
st_2_list

# %%
# mean sum of temperatures at the beginning of the growing season
np.mean(st_1_list)

# %%
# mean sum of temperatures at the end of the growing season
np.mean(st_2_list)

# %% [markdown]
# ## Shannon Airport, Co. Clare
#
# <https://data.gov.ie/dataset/shannon-airport-daily-data>

# %%
URL = "https://cli.fusio.net/cli/climate_data/webdata/dly518.csv"
SUB_DIR = os.path.join(DATA_DRIVE, "MetEireann")
KNOWN_HASH = "bf3eaaa3f060f548540cb463c81ef886472eea4d03e011c60f7ac82d82f61bfb"
os.makedirs(SUB_DIR, exist_ok=True)
FILE_NAME = "dly518.csv"

# %%
pooch.retrieve(
    url=URL,
    known_hash=KNOWN_HASH,
    fname=FILE_NAME,
    path=SUB_DIR
)

# %%
dat = pd.read_csv(
    os.path.join(SUB_DIR, FILE_NAME), skiprows=24, parse_dates=["date"]
)

# %%
dat.head()

# %%
# keep only min and max air temps
dat = dat[["date", "maxtp", "mintp"]]

# %%
# filter data for 1954 - 1968
dat = dat[(dat["date"].dt.year >= 1954) & (dat["date"].dt.year <= 1968)]

# %%
dat.head()

# %%
# calculate mean air temperature
dat["meantp"] = dat[["maxtp", "mintp"]].mean(axis=1)

# %%
# keep only mean and date columns
dat = dat[["date", "meantp"]]

# %%
# return only mean values above 4, and subtract by 4
dat.loc[(dat["meantp"] >= 4.0), "tgrowth"] = dat["meantp"] - 4.0

# %%
dat.head()

# %%
# extract data to determine beginning of growing season
st_1 = {}
for y in dat["date"].dt.year.unique():
    st_1[y] = dat[
        (dat["date"] >= f"{y}-01-01") & (dat["date"] <= f"{y}-03-06")
    ]

# %%
# extract data to determine end of growing season
st_2 = {}
for y in dat["date"].dt.year.unique():
    st_2[y] = dat[
        (dat["date"] >= f"{y}-01-01") & (dat["date"] <= f"{y}-12-08")
    ]

# %%
# sum of temperatures at the beginning
st_1_list = []
for y in st_1.keys():
    st_1_list.append(list(st_1[y]["tgrowth"].cumsum())[-1])
# remove NaN
st_1_list = [n for n in st_1_list if str(n) != "nan"]

# %%
# sum of temperatures at the end
st_2_list = []
for y in st_2.keys():
    st_2_list.append(list(st_2[y]["tgrowth"].cumsum())[-1])
# remove NaN
st_2_list = [n for n in st_2_list if str(n) != "nan"]

# %%
st_1_list

# %%
st_2_list

# %%
np.mean(st_1_list)

# %%
np.mean(st_2_list)

# %% [markdown]
# ## Rosslare, Co. Wexford
#
# <https://data.gov.ie/dataset/rosslare-daily-data>

# %%
URL = "https://cli.fusio.net/cli/climate_data/webdatac/dly2615.csv"
SUB_DIR = os.path.join(DATA_DRIVE, "MetEireann")
KNOWN_HASH = "e37a2f84e4172329cd178fc7bddb9720ca559c5c0777bf87cd2b5a42af62c226"
os.makedirs(SUB_DIR, exist_ok=True)
FILE_NAME = "dly2615.csv"

# %%
pooch.retrieve(
    url=URL,
    known_hash=KNOWN_HASH,
    fname=FILE_NAME,
    path=SUB_DIR
)

# %%
dat = pd.read_csv(
    os.path.join(SUB_DIR, FILE_NAME), skiprows=17, skipfooter=1,
    parse_dates=["date"], engine="python"
)

# %%
dat.head()

# %%
# keep only min and max air temps
dat = dat[["date", "maxtp", "mintp"]]

# %%
# filter data for 1954 - 1968
dat = dat[(dat["date"].dt.year >= 1954) & (dat["date"].dt.year <= 1968)]

# %%
dat.tail()

# %%
# calculate mean air temperature
dat["meantp"] = dat[["maxtp", "mintp"]].mean(axis=1)

# %%
# keep only mean and date columns
dat = dat[["date", "meantp"]]

# %%
# return only mean values above 4, and subtract by 4
dat.loc[(dat["meantp"] >= 4.0), "tgrowth"] = dat["meantp"] - 4.0

# %%
dat.head()

# %%
# extract data to determine beginning of growing season
st_1 = {}
for y in dat["date"].dt.year.unique():
    if y > 1956:
        st_1[y] = dat[
            (dat["date"] >= f"{y}-01-01") & (dat["date"] <= f"{y}-02-28")
        ]

# %%
# extract data to determine end of growing season
st_2 = {}
for y in dat["date"].dt.year.unique():
    if y > 1956:
        st_2[y] = dat[
            (dat["date"] >= f"{y}-01-01") & (dat["date"] <= f"{y}-12-19")
        ]

# %%
# sum of temperatures at the beginning
st_1_list = []
for y in st_1.keys():
    st_1_list.append(list(st_1[y]["tgrowth"].cumsum())[-1])
# remove NaN
st_1_list = [n for n in st_1_list if str(n) != "nan"]

# %%
# sum of temperatures at the end
st_2_list = []
for y in st_2.keys():
    st_2_list.append(list(st_2[y]["tgrowth"].cumsum())[-1])
# remove NaN
st_2_list = [n for n in st_2_list if str(n) != "nan"]

# %%
st_1_list

# %%
st_2_list

# %%
np.mean(st_1_list)

# %%
np.mean(st_2_list)
