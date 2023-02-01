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

## Notebooks

### Main

Notebook | Link
--- | ---
***Boundary***
Ireland boundary - NUTS 2021 | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/ireland-boundary-nuts.ipynb)
***Meteorological data***
Sample met data (Valentia Observatory) for model development | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/sample-met-data.ipynb)
***EURO-CORDEX***
EURO-CORDEX data catalogue | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/eurocordex-intake.ipynb)
EURO-CORDEX data for Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/eurocordex-ie.ipynb)
***Grass growth***
ModVege results using sample met data | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/modvege-valentia.ipynb)
ModVege results with EURO-CORDEX data | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/modvege.ipynb)
***Livestock units***
Census of Agriculture 2020, CSO | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/agricultural_census_cso.ipynb)

### Other

Notebook | Link
--- | ---
***Boundary***
Ireland boundary - Ordnance Survey Ireland / Northern Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/ireland-boundary.ipynb)
***Land use and soil***
CORINE land cover 2018 | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/clc-2018.ipynb)
Soil information system | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/irish-soil-information-system.ipynb)
***Meteorological data***
Met stations in Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/met-stations.ipynb)
Met Éireann Reanalysis | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/mera-data.ipynb)
***HiResIreland***
HiResIreland climate model data | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/hiresireland.ipynb)
***Grass growth***
GrassCheck NI | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/grasscheck.ipynb)
PastureBase Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/pasturebase.ipynb)
Grass10 | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/grass10.ipynb)
Growing season definition based on Connaughton (1973) | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/sample-met-data.ipynb)
***Climatic regions***
Seasonality map from EPA phenology study by Scarrott et al. (2010) | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/seasonality-map-epa.ipynb)
Agro-environmental regions based on February rainfall by Holden and Brereton (2004) | [nbviewer](https://nbviewer.org/gist/nmstreethran/153a21ee6d6d68c98de2de9867cf254d/agro-environmental-regions.ipynb)

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
