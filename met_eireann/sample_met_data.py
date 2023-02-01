# %% [markdown]
# # Sample met data for testing ModVege
#
# Data used: Met Eireann daily data for Valentia Observatory, Co. Kerry
# (<https://data.gov.ie/dataset/valentia-observatory-daily-data>)

# %%
import os
from datetime import datetime, timezone
import pandas as pd
import pooch

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DRIVE = "data"
URL = "https://cli.fusio.net/cli/climate_data/webdata/dly2275.csv"
SUB_DIR = os.path.join(DATA_DRIVE, "MetEireann")
KNOWN_HASH = None
os.makedirs(SUB_DIR, exist_ok=True)
FILE_NAME = "dly2275.csv"

# %%
# download data if it doesn't exist
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
val = pd.read_csv(
    os.path.join(SUB_DIR, FILE_NAME), skiprows=24, parse_dates=["date"]
)

# %%
val.head()

# %%
# filter data for 2019 - 2021
val = val[(val["date"].dt.year >= 2019) & (val["date"].dt.year <= 2021)]

# %%
val.sort_values(by=["date"], inplace=True)
val.reset_index(inplace=True)

# %%
# keep only min and max air temps, rainfall, global radiation, PET
val = val[["date", "maxtp", "mintp", "rain", "glorad", "pe"]]

# %%
val.head()

# %%
# calculate mean air temperature
val["T"] = val[["maxtp", "mintp"]].mean(axis=1)

# %%
# convert global radiation units to MJ m-2 from J cm-2
# see Allen et al. (1998)
val["RG"] = val["glorad"].astype(float) / 100.0

# %%
# convert global radiation to PAR
# see Papaioannou et al. (1993)
val["PAR"] = val["RG"] * 0.473

# %%
# rainfall
val["PP"] = val["rain"].astype(float)

# %%
# potential evapotranspiration
val["PET"] = val["pe"].astype(float)

# %%
val["time"] = val["date"]

# %%
# keep only relevant columns
val = val[["time", "T", "PAR", "PET", "PP", "RG"]]

# %%
val.head()

# %%
val.tail()

# %%
# save as a CSV file
val.to_csv(os.path.join(SUB_DIR, "valentia.csv"), index=False)
