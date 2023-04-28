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
- [Ireland counties - Ordnance Survey Ireland / Northern Ireland](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/boundaries/ireland_boundary.ipynb)
- [Natural Earth 10 m boundary for Ireland](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/boundaries/naturalearth.ipynb)

### Climate model datasets (EURO-CORDEX and HiResIreland)

- [EURO-CORDEX data catalogue](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/eurocordex/eurocordex_intake.ipynb)
- [EURO-CORDEX data for Ireland](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/eurocordex/eurocordex_ie.ipynb)
- [HiResIreland data fields](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/hiresireland/hiresireland_fields.ipynb)
- [HiResIreland data](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/hiresireland/hiresireland.ipynb)
- [Dataset visualisations](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/climate_data/climate_data_viz.ipynb)

### Met Éireann Reanalysis (MÉRA)

- [Using MÉRA GRIB files](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/mera/mera_data.ipynb)
- [MÉRA data comparison with met station observations](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/mera/mera_data_compare.ipynb)
- [Deriving evapotranspiration using MÉRA](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/mera/mera_data_et.ipynb)
- [Processed MÉRA data](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/mera/mera_data_process.ipynb)
- [Handle missing MÉRA data](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/mera/mera_data_missing.ipynb)

### Meteorological data

- [Sample met data (Valentia Observatory) for model development](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/met/sample_met_data.ipynb)
- [Met stations in Ireland](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/met/met_stations.ipynb)

### Livestock units

- Census of Agriculture: [CSO](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/agricultural_census/agricultural_census_cso.ipynb), [DAERA](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/agricultural_census/agricultural_census_daera.ipynb)
- [Census of Agriculture - geospatial data](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/agricultural_census/agricultural_census.ipynb)
- Census of Agriculture - gridded data: [EURO-CORDEX](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/agricultural_census/agricultural_census_gridded_eurocordex.ipynb), [HiResIreland](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/agricultural_census/agricultural_census_gridded_hiresireland.ipynb), [MÉRA](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/agricultural_census/agricultural_census_gridded_mera.ipynb)

### Soil

- Nitrogen nutritional index based on LUCAS topsoil data: [EURO-CORDEX](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/soil_nitrogen/nitrogen_lucas_topsoil_eurocordex.ipynb), [HiResIreland](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/soil_nitrogen/nitrogen_lucas_topsoil_hiresireland.ipynb), [MÉRA](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/soil_nitrogen/nitrogen_lucas_topsoil_mera.ipynb)
- Soil water-holding capacity based on European soil database derived data: [EURO-CORDEX](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/soil_water_content/soil_water_content_eurocordex.ipynb), [HiResIreland](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/soil_water_content/soil_water_content_hiresireland.ipynb), [MÉRA](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/soil_water_content/soil_water_content_mera.ipynb)

### Grass growth observations

- [PastureBase Ireland](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/grass_growth/pasturebase.ipynb)
- [GrassCheck NI](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/grass_growth/grasscheck.ipynb)

### Land cover

- [CORINE Land Cover 2018](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/land_cover/clc_2018.ipynb)

### Data preparation

- [Comparison of regridding methods](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/modvege/regridding.ipynb)
- [Prepare MÉRA time series for model evaluation](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/grass_growth/grass_growth_mera_ts.ipynb)

### Future risk (historical with future)

#### Seasonal

- EURO-CORDEX: [mean](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_exp_mean/modvege_eurocordex_compare_exp_diff_mean.ipynb), [std](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_exp_std/modvege_eurocordex_compare_exp_diff_std.ipynb), [max](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_exp_max/modvege_eurocordex_compare_exp_diff_max.ipynb), [min](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_exp_min/modvege_eurocordex_compare_exp_diff_min.ipynb)
- HiResIreland: [mean](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_exp_mean/modvege_hiresireland_compare_exp_diff_mean.ipynb), [std](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_exp_std/modvege_hiresireland_compare_exp_diff_std.ipynb), [max](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_exp_max/modvege_hiresireland_compare_exp_diff_max.ipynb), [min](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_exp_min/modvege_hiresireland_compare_exp_diff_min.ipynb)

#### Annual / overall

- EURO-CORDEX: [mean](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_exp_mean/modvege_eurocordex_compare_exp_diff_mean_annual.ipynb), [std](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_exp_std/modvege_eurocordex_compare_exp_diff_std_annual.ipynb), [max](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_exp_max/modvege_eurocordex_compare_exp_diff_max_annual.ipynb), [min](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_exp_min/modvege_eurocordex_compare_exp_diff_min_annual.ipynb)
- HiResIreland: [mean](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_exp_mean/modvege_hiresireland_compare_exp_diff_mean_annual.ipynb), [std](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_exp_std/modvege_hiresireland_compare_exp_diff_std_annual.ipynb), [max](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_exp_max/modvege_hiresireland_compare_exp_diff_max_annual.ipynb), [min](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_exp_min/modvege_hiresireland_compare_exp_diff_min_annual.ipynb)

### Validation

- EURO-CORDEX: [mean](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_mera_mean/modvege_eurocordex_compare_mera_diff_mean.ipynb), [std](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_mera_std/modvege_eurocordex_compare_mera_diff_std.ipynb), [max](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_mera_max/modvege_eurocordex_compare_mera_diff_max.ipynb), [min](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_mera_min/modvege_eurocordex_compare_mera_diff_min.ipynb)
- HiResIreland: [mean](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_mera_mean/modvege_hiresireland_compare_mera_diff_mean.ipynb), [std](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_mera_std/modvege_hiresireland_compare_mera_diff_std.ipynb), [max](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_mera_max/modvege_hiresireland_compare_mera_diff_max.ipynb), [min](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_mera_min/modvege_hiresireland_compare_mera_diff_min.ipynb)

<!-- #### Annual / overall

- EURO-CORDEX: [mean](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_mera_mean/modvege_eurocordex_compare_mera_diff_mean_annual.ipynb), [std](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_mera_std/modvege_eurocordex_compare_mera_diff_std_annual.ipynb), [max](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_mera_max/modvege_eurocordex_compare_mera_diff_max_annual.ipynb), [min](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_mera_min/modvege_eurocordex_compare_mera_diff_min_annual.ipynb)
- HiResIreland: [mean](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_mera_mean/modvege_hiresireland_compare_mera_diff_mean_annual.ipynb), [std](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_mera_std/modvege_hiresireland_compare_mera_diff_std_annual.ipynb), [max](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_mera_max/modvege_hiresireland_compare_mera_diff_max_annual.ipynb), [min](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/stats_compare_mera_min/modvege_hiresireland_compare_mera_diff_min_annual.ipynb) -->

### Model evaluation

- [Compare simulations with grass growth measurements](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/grass_growth/grass_growth_pastures_compare.ipynb)

### Model results

- [ModVege results using sample met data](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/modvege/modvege_valentia.ipynb)
- [ModVege results with EURO-CORDEX data](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/modvege/modvege_eurocordex.ipynb)
- [ModVege results with HiResIreland data](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/modvege/modvege_hiresireland.ipynb)
- [Moorepark time series distribution](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/modvege/modvege_timeseries_moorepark.ipynb)

### Other

- [Irish Soil Information System](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/soil/irish_soil_information_system.ipynb)
- [Grass10](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/grass_growth/grass10.ipynb)
- [Seasonality map from EPA phenology study by Scarrott et al. (2010)](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/climatic_regions/seasonality_map_epa.ipynb)
- [Agro-environmental regions based on February rainfall by Holden and Brereton (2004)](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/climatic_regions/agro_environmental_regions.ipynb)
- [Growing season definition based on Connaughton (1973)](https://nbviewer.org/github/ClimAg/jupyter-notebooks/blob/ipynb/met/met_growing_season.ipynb)

<!--
## References

- Coordinate reference system for Ireland: [ETRS89 / Irish TM EPSG 2157](https://www.gov.uk/government/publications/uk-geospatial-data-standards-register/national-geospatial-data-standards-register#standards-for-coordinate-reference-systems)
-->

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
