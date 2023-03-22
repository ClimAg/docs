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

Windows users should use Conda within Windows Subsystem for Linux (WSL), as some packages (e.g. cdo) are unavailable for Windows.

## Notebooks

### Main

Notebook | Link
--- | ---
***Boundary***
Ireland boundary - NUTS 2021 | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/ireland_boundary_nuts.ipynb)
Ireland Electoral Divisions | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/ireland_boundary_electoral_divisions.ipynb)
Northern Ireland Electoral Wards | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/ireland_boundary_ni_wards.ipynb)
Ireland counties - Ordnance Survey Ireland / Northern Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/ireland-boundary.ipynb)
Natural Earth 10 m boundary for Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/naturalearth.ipynb)
***Meteorological data***
Sample met data (Valentia Observatory) for model development | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/sample_met_data.ipynb)
***Climate model datasets***
EURO-CORDEX data catalogue | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/eurocordex_intake.ipynb)
EURO-CORDEX data for Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/eurocordex_ie.ipynb)
HiResIreland data | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/hiresireland.ipynb)
HiResIreland variables | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/hiresireland_fields.ipynb)
Dataset visualisations | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/climate_data_viz.ipynb)
***Met Éireann Reanalysis***
Met Éireann Reanalysis | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/mera_data.ipynb)
MÉRA accumulated data comparison | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/mera_data_accumulated.ipynb)
***Model results***
ModVege results using sample met data | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/modvege_valentia.ipynb)
ModVege results with EURO-CORDEX data | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/modvege_eurocordex.ipynb)
ModVege results with HiResIreland data | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/modvege_hiresireland.ipynb)
EURO-CORDEX hist/rcp result comparisons | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/modvege_eurocordex_hist_rcp.ipynb)
Moorepark time series distribution | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/modvege_timeseries_moorepark.ipynb)
***Livestock units***
Census of Agriculture, CSO | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/agricultural_census_cso.ipynb)
Census of Agriculture, DAERA | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/agricultural_census_daera.ipynb)
Census of Agriculture - geospatial data | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/agricultural_census.ipynb)
Census of Agriculture - gridded data - EURO-CORDEX | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/agricultural_census_gridded_eurocordex.ipynb)
Census of Agriculture - gridded data - HiResIreland | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/agricultural_census_gridded_hiresireland.ipynb)
***Soil***
Nitrogen nutritional index based on LUCAS topsoil data - EURO-CORDEX | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/nitrogen_lucas_topsoil_eurocordex.ipynb)
Nitrogen nutritional index based on LUCAS topsoil data - HiResIreland | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/nitrogen_lucas_topsoil_hiresireland.ipynb)
Soil water-holding capacity based on European soil database derived data - EURO-CORDEX | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/soil_water_content_eurocordex.ipynb)
Soil water-holding capacity based on European soil database derived data - HiResIreland | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/soil_water_content_hiresireland.ipynb)
***Meteorological data***
Met stations in the Island of Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/met-stations.ipynb)
***Grass growth***
GrassCheck NI | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/grasscheck.ipynb)
PastureBase Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/pasturebase.ipynb)
***Climatic regions***
Seasonality map from EPA phenology study by Scarrott et al. (2010) | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/seasonality-map-epa.ipynb)
Agro-environmental regions based on February rainfall by Holden and Brereton (2004) | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/agro-environmental-regions.ipynb)

### Other

Notebook | Link
--- | ---
***Land use and soil***
CORINE land cover 2018 | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/clc-2018.ipynb)
Soil information system | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/irish-soil-information-system.ipynb)
***Grass growth***
Grass10 | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/grass10.ipynb)
Growing season definition based on Connaughton (1973) | [nbviewer](https://nbviewer.org/gist/nmstreethran/88adb3d843260d60e038dafdbf3c4c41/sample-met-data.ipynb)

## References

- Coordinate reference system for Ireland: [ETRS89 / Irish TM EPSG 2157](https://www.gov.uk/government/publications/uk-geospatial-data-standards-register/national-geospatial-data-standards-register#standards-for-coordinate-reference-systems)

## Licence

Copyright 2022 N. M. Streethran

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  <https://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
