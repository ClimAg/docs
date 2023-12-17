#!/usr/bin/env python
# coding: utf-8

# # ModVege grass growth model (Jouven et al. 2006)
#
# - Jouven, M., Carrère, P., and Baumont, R. (2006a). 'Model predicting
#   dynamics of biomass, structure and digestibility of herbage in managed
#   permanent pastures. 1. Model description', *Grass and Forage Science*,
#   vol. 61, no. 2, pp. 112-124. DOI:
#   [10.1111/j.1365-2494.2006.00515.x][Jouven1].
# - Jouven, M., Carrère, P., and Baumont, R. (2006b). 'Model predicting
#   dynamics of biomass, structure and digestibility of herbage in managed
#   permanent pastures. 2. Model evaluation', *Grass and Forage Science*,
#   vol. 61, no. 2, pp. 125-133. DOI:
#   [10.1111/j.1365-2494.2006.00517.x][Jouven2].
# - Chemin, Y. (2022). 'modvege', Python. [Online]. Available at
#   <https://github.com/YannChemin/modvege> (Accessed 6 September 2022).
#
# [Jouven1]: https://doi.org/10.1111/j.1365-2494.2006.00515.x
# [Jouven2]: https://doi.org/10.1111/j.1365-2494.2006.00517.x

import os
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from climag.modvege_run import run_modvege

DATA_DIR = os.path.join("data", "ModVege")

# define the name of the input params file
PARAMS_FILE = os.path.join(DATA_DIR, "params.csv")

# define the name of the input time series file
TS_FILE = os.path.join("data", "met", "MetEireann", "valentia.csv")

# ## Input time series

ts = pd.read_csv(TS_FILE, parse_dates=["time"])

ts.sort_values(by=["time"], inplace=True)
ts = ts.reset_index().set_index("time")

ts.head()

ts.tail()

for year in ts.index.year.unique():
    print("T", year, round(np.mean(ts.loc[str(year)]["T"]), 2))
    print("PP", year, round(np.mean(ts.loc[str(year)]["PP"]), 2))
    print(
        "grazing season length",
        round(
            29.3 * np.mean(ts.loc[str(year)]["T"])
            - 0.1 * np.sum(ts.loc[str(year)]["PP"])
            + 19.5
        ),
    )

# ## Results for different residual grass heights

# ### h = 0.05 m

# run the main function using the example data
# rep = 0 when grazed/harvested
run_modvege(
    input_params_file=PARAMS_FILE,
    input_timeseries_file=TS_FILE,
    out_dir=DATA_DIR,
)

# ### h = 0.00 m (max cutting)

run_modvege(
    input_params_file=PARAMS_FILE,
    input_timeseries_file=TS_FILE,
    out_dir=DATA_DIR,
)

# ### h = None (no cutting)

run_modvege(
    input_params_file=PARAMS_FILE,
    input_timeseries_file=TS_FILE,
    out_dir=DATA_DIR,
)

# ## Using the original definition of LAI

# ### h = 0.05 m

run_modvege(
    input_params_file=PARAMS_FILE,
    input_timeseries_file=TS_FILE,
    out_dir=DATA_DIR,
)

# ### h = 0.00 m (max cutting)

run_modvege(
    input_params_file=PARAMS_FILE,
    input_timeseries_file=TS_FILE,
    out_dir=DATA_DIR,
)

# ### h = None (no cutting)

run_modvege(
    input_params_file=PARAMS_FILE,
    input_timeseries_file=TS_FILE,
    out_dir=DATA_DIR,
)
