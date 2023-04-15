# jupyter-notebooks

Jupyter notebooks for the [ClimAg](https://www.ucc.ie/en/eel/projects/climag/) research project

This research was funded by the Environmental Protection Agency (EPA), Ireland
project "ClimAg: Multifactorial causes of fodder crises in Ireland and risks
due to climate change" under the Climate Change Research Programme grant
number 2018-CCRP-MS.50.

## Python environment

Create a Conda environment:

```sh
conda env create
conda activate ClimAg
```

To update the environment:

```sh
conda env update --name ClimAg --file environment.yml
```

Windows users should use Conda within Windows Subsystem for Linux (WSL), as some packages (e.g. CDO) are unavailable for Windows.

## Notebooks

### Boundaries

- [Ireland boundary - NUTS 2021](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/boundaries/ireland_boundary_nuts.ipynb)
- [Ireland Electoral Divisions](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/boundaries/ireland_boundary_electoral_divisions.ipynb)
- [Northern Ireland Electoral Wards](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/boundaries/ireland_boundary_ni_wards.ipynb)
- [Ireland counties - Ordnance Survey Ireland / Northern Ireland](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/boundaries/ireland-boundary.ipynb)
- [Natural Earth 10 m boundary for Ireland](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/boundaries/naturalearth.ipynb)

### HiResIreland

- [HiResIreland data fields](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/hiresireland/hiresireland_fields.ipynb)

### Met Éireann Reanalysis (MÉRA)

- [Using MÉRA GRIB files](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/mera/mera_data.ipynb)
- [MÉRA data comparison with met station observations](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/mera/mera_data_compare.ipynb)
- [Deriving evapotranspiration using MÉRA](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/mera/mera_data_et.ipynb)
- [Processed MÉRA data](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/mera/mera_data_process.ipynb)

### Meteorological data

- [Sample met data (Valentia Observatory) for model development](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/met/sample_met_data.ipynb)
- [Met stations in Ireland](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/met/met_stations.ipynb)

### Livestock units

- Census of Agriculture: [CSO](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/agricultural_census/agricultural_census_cso.ipynb), [DAERA](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/agricultural_census/agricultural_census_daera.ipynb)
- [Census of Agriculture - geospatial data](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/agricultural_census/agricultural_census.ipynb)
- Census of Agriculture - gridded data: [EURO-CORDEX](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/agricultural_census/agricultural_census_gridded_eurocordex.ipynb), [HiResIreland](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/agricultural_census/agricultural_census_gridded_hiresireland.ipynb), [MÉRA](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/agricultural_census/agricultural_census_gridded_mera.ipynb)

### Soil

- Nitrogen nutritional index based on LUCAS topsoil data: [EURO-CORDEX](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/soil/nitrogen/nitrogen_lucas_topsoil_eurocordex.ipynb), [HiResIreland](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/soil/nitrogen/nitrogen_lucas_topsoil_hiresireland.ipynb), [MÉRA](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/soil/nitrogen/nitrogen_lucas_topsoil_mera.ipynb)
- Soil water-holding capacity based on European soil database derived data: [EURO-CORDEX](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/soil/water_content/soil_water_content_eurocordex.ipynb), [HiResIreland](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/soil/water_content/soil_water_content_hiresireland.ipynb), [MÉRA](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/soil/water_content/soil_water_content_mera.ipynb)
- [Irish Soil Information System](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/soil/irish_soil_information_system.ipynb)

### Grass growth observations

- [PastureBase Ireland](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/grass_growth/pasturebase.ipynb)
- [GrassCheck NI](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/grass_growth/grasscheck.ipynb)
- [Grass10](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/grass_growth/grass10.ipynb)

### Land cover

- [CORINE Land Cover 2018](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/land_cover/clc_2018.ipynb)

### Data preparation

- [Comparison of regridding methods](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/modvege/regridding.ipynb)

### Compare simulation results (historical with future)

- EURO-CORDEX: [mean](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats/compare_exp/mean/modvege_eurocordex_compare_exp_diff_mean.ipynb), [std](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats/compare_exp/std/modvege_eurocordex_compare_exp_diff_std.ipynb), [max](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats/compare_exp/max/modvege_eurocordex_compare_exp_diff_max.ipynb), [min](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats/compare_exp/min/modvege_eurocordex_compare_exp_diff_min.ipynb)
- HiResIreland: [mean](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats/compare_exp/mean/modvege_hiresireland_compare_exp_diff_mean.ipynb), [std](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats/compare_exp/std/modvege_hiresireland_compare_exp_diff_std.ipynb), [max](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats/compare_exp/max/modvege_hiresireland_compare_exp_diff_max.ipynb), [min](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats/compare_exp/min/modvege_hiresireland_compare_exp_diff_min.ipynb)

### Compare simulation results (historical with observations)

- EURO-CORDEX: [mean](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats/compare_mera/mean/modvege_eurocordex_compare_mera_diff_mean.ipynb), [std](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats/compare_mera/std/modvege_eurocordex_compare_mera_diff_std.ipynb), [max](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats/compare_mera/max/modvege_eurocordex_compare_mera_diff_max.ipynb), [min](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats/compare_mera/min/modvege_eurocordex_compare_mera_diff_min.ipynb)
- HiResIreland: [mean](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats/compare_mera/mean/modvege_hiresireland_compare_mera_diff_mean.ipynb), [std](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats/compare_mera/std/modvege_hiresireland_compare_mera_diff_std.ipynb), [max](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats/compare_mera/max/modvege_hiresireland_compare_mera_diff_max.ipynb), [min](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats/compare_mera/min/modvege_hiresireland_compare_mera_diff_min.ipynb)

<!--
***Climate model datasets***
EURO-CORDEX data catalogue | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/eurocordex_intake.ipynb)
EURO-CORDEX data for Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/eurocordex_ie.ipynb)
HiResIreland data | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/hiresireland.ipynb)
HiResIreland variables | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/hiresireland_fields.ipynb)
Dataset visualisations | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/climate_data_viz.ipynb)
***Met Éireann Reanalysis***
Create MÉRA ModVege input data | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/mera_data_process.ipynb)
***Model results***
ModVege results using sample met data | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/modvege_valentia.ipynb)
ModVege results with EURO-CORDEX data | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/modvege_eurocordex.ipynb)
ModVege results with HiResIreland data | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/modvege_hiresireland.ipynb)
Moorepark time series distribution | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/modvege_timeseries_moorepark.ipynb)
***Meteorological data***
Met stations in the Island of Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/met-stations.ipynb)
***Grass growth***
GrassCheck NI | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/grasscheck.ipynb)
PastureBase Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/pasturebase.ipynb)
***Climatic regions***
Seasonality map from EPA phenology study by Scarrott et al. (2010) | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/seasonality-map-epa.ipynb)
Agro-environmental regions based on February rainfall by Holden and Brereton (2004) | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/agro-environmental-regions.ipynb)

### Other

***Land use and soil***
CORINE land cover 2018 | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/clc-2018.ipynb)
Soil information system | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/irish-soil-information-system.ipynb)
***Grass growth***
Grass10 | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/grass10.ipynb)
Growing season definition based on Connaughton (1973) | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/sample-met-data.ipynb)

## References

- Coordinate reference system for Ireland: [ETRS89 / Irish TM EPSG 2157](https://www.gov.uk/government/publications/uk-geospatial-data-standards-register/national-geospatial-data-standards-register#standards-for-coordinate-reference-systems) -->

## Licence

Copyright 2022-2023 N. M. Streethran

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  <https://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
