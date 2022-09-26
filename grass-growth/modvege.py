# %% [markdown]
# # ModVege grass growth model (Jouven et al. 2006)
#
# - Jouven, M., Carrère, P. and Baumont, R. (2006). ‘Model predicting dynamics of biomass, structure and digestibility of herbage in managed permanent pastures. 1. Model description’, Grass and Forage Science, vol. 61, no. 2, pp. 112–124. DOI: [10.1111/j.1365-2494.2006.00515.x](https://doi.org/10.1111/j.1365-2494.2006.00515.x).
# - Jouven, M., Carrère, P. and Baumont, R. (2006). ‘Model predicting dynamics of biomass, structure and digestibility of herbage in managed permanent pastures. 2. Model evaluation’, Grass and Forage Science, vol. 61, no. 2, pp. 125–133. DOI: [10.1111/j.1365-2494.2006.00517.x](https://doi.org/10.1111/j.1365-2494.2006.00517.x).
# - Chemin, Y. (2022). ‘modvege’, Python. [Online]. Available at <https://github.com/YannChemin/modvege> (Accessed 6 September 2022).

# %%
import os
from climag.modvege_run import run_modvege

# %%
DATA_PATH = os.path.join("data", "grass-growth", "modvege")

# define the name of the input params file (using example data for now)
PARAMS_FILE = os.path.join(DATA_PATH, "params.csv")
# define the name of the input environment file
WEATHER_FILE = os.path.join(DATA_PATH, "weather.csv")
# outputs
OUT_FILE = os.path.join(DATA_PATH, "output.csv")

# %%
# run the main function using the example data
run_modvege(
    input_params_csv=PARAMS_FILE,
    input_weather_csv=WEATHER_FILE,
    out_csv=OUT_FILE
)
