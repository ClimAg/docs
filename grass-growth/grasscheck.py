# %%
import os
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import pandas as pd
import climag.plot_configs

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
DATA_DIR = os.path.join("data", "grasscheck", "grasscheck.csv")

# %%
grass_ni = pd.read_csv(DATA_DIR, parse_dates=["week"], dayfirst=True)

# %%
grass_ni.shape

# %%
grass_ni.head()

# %%
grass_ni.plot(x="week", figsize=(14, 5), linewidth=1)
plt.title("Grass growth data from GrassCheck in Northern Ireland")
plt.xlabel("Time")
plt.ylabel("Grass growth (kg DM/ha/d)")
plt.show()
