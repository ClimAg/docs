# %% [markdown]
# # Census of Agriculture

# %%
import os
from datetime import datetime, timezone
import pandas as pd
import pooch

# %% [markdown]
# ## Farms with Livestock
#
# <https://data.cso.ie/table/AVA42>

# %%
URL = (
    "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/"
    "AVA42/CSV/1.0/en"
)
KNOWN_HASH = None
FILE_NAME = "COA_2020_AVA42.csv"
SUB_DIR = os.path.join("data", "AgriculturalCensus", "CSO")
DATA_FILE = os.path.join(SUB_DIR, FILE_NAME)
os.makedirs(SUB_DIR, exist_ok=True)

# %%
# download data if necessary
if not os.path.isfile(os.path.join(SUB_DIR, FILE_NAME)):
    pooch.retrieve(
        url=URL,
        known_hash=KNOWN_HASH,
        fname=FILE_NAME,
        path=SUB_DIR
    )

    with open(
        os.path.join(SUB_DIR, f"{FILE_NAME[:-4]}.txt"), "w", encoding="utf-8"
    ) as outfile:
        outfile.write(
            f"Data downloaded on: {datetime.now(tz=timezone.utc)}\n"
            f"Download URL: {URL}"
        )

# %%
coa = pd.read_csv(DATA_FILE)

# %%
coa.head()

# %%
# filter for 2020, for total cattle and total sheep
# drop the state numbers
coa = coa[coa["Census Year"] == 2020]
coa = coa[coa["Type of Livestock"].isin(["Total cattle", "Total sheep"])]
coa = coa[coa["Electoral Division"] != "State"]

# %%
coa.head()

# %%
# drop unnecessary columns
coa.drop(
    columns=[
        "STATISTIC", "Statistic Label", "TLIST(A1)",
        "C02148V02965", "UNIT", "Census Year"
    ],
    inplace=True
)

# %%
# split cattle and sheep values into separate columns
coa = pd.merge(
    coa[coa["Type of Livestock"] == "Total cattle"],
    coa[coa["Type of Livestock"] == "Total sheep"],
    on=["C03904V04656", "Electoral Division"]
)

# %%
coa.head()

# %%
# rename columns
coa.rename(
    columns={
        "Electoral Division": "electoral_division",
        "VALUE_x": "total_cattle",
        "VALUE_y": "total_sheep"
    },
    inplace=True
)

# %%
# drop unnecessary columns
coa.drop(columns=["Type of Livestock_x", "Type of Livestock_y"], inplace=True)

# %%
coa.head()

# %% [markdown]
# ## Land Utilisation
#
# <https://data.cso.ie/table/AVA44>

# %%
URL = (
    "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/"
    "AVA44/CSV/1.0/en"
)
KNOWN_HASH = None
FILE_NAME = "COA_2020_AVA44.csv"
SUB_DIR = os.path.join("data", "AgriculturalCensus", "CSO")
DATA_FILE = os.path.join(SUB_DIR, FILE_NAME)
os.makedirs(SUB_DIR, exist_ok=True)

# %%
# download data if necessary
if not os.path.isfile(os.path.join(SUB_DIR, FILE_NAME)):
    pooch.retrieve(
        url=URL,
        known_hash=KNOWN_HASH,
        fname=FILE_NAME,
        path=SUB_DIR
    )

    with open(
        os.path.join(SUB_DIR, f"{FILE_NAME[:-4]}.txt"), "w", encoding="utf-8"
    ) as outfile:
        outfile.write(
            f"Data downloaded on: {datetime.now(tz=timezone.utc)}\n"
            f"Download URL: {URL}"
        )

# %%
land = pd.read_csv(DATA_FILE)

# %%
land.head()

# %%
# filter for 2020, for all grassland
# drop the state numbers
land = land[land["Census Year"] == 2020]
land = land[land["Type of Crop"] == "All grassland"]
land = land[land["Electoral Division"] != "State"]

# %%
land.head()

# %%
# rename columns
land.rename(
    columns={
        "Electoral Division": "electoral_division",
        "VALUE": "all_grassland_hectares"
    },
    inplace=True
)

# %%
land

# %%
# keep only necessary columns
land = land[["C03904V04656", "electoral_division", "all_grassland_hectares"]]

# %%
land.head()

# %% [markdown]
# ## Merge datasets

# %%
data = pd.merge(coa, land, on=["C03904V04656", "electoral_division"])

# %%
data.head()

# %%
# save as a CSV file
data.to_csv(os.path.join(SUB_DIR, "COA_2020.csv"), index=False)
