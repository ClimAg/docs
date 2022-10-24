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

`environment.yml`:

```yml
name: ClimAg
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - dask
  - matplotlib
  - rioxarray
  - geopandas
  - intake-esm
  - cartopy
  - nc-time-axis
  - jupyterlab
  - aiohttp
  - odfpy
  - seaborn
```

## Notebooks

Notebook | Link
--- | ---
***Boundary***
Ireland boundary - NUTS 2021 | [nbviewer](https://nbviewer.org/gist/nmstreethran/6afcd31bfe1c328d05056d031d1ba8f5/ireland-boundary-nuts.ipynb)
Ireland boundary - Ordnance Survey Ireland / Northern Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/6afcd31bfe1c328d05056d031d1ba8f5/ireland-boundary.ipynb)
***Land use and soil***
CORINE land cover 2018 | [nbviewer](https://nbviewer.org/gist/nmstreethran/6afcd31bfe1c328d05056d031d1ba8f5/clc-2018.ipynb)
Soil information system | [nbviewer](https://nbviewer.org/gist/nmstreethran/6afcd31bfe1c328d05056d031d1ba8f5/irish-soil-information-system.ipynb)
***Meteorological data***
Met stations in Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/6afcd31bfe1c328d05056d031d1ba8f5/met-stations.ipynb)
***HiResIreland***
HiResIreland climate model data | [nbviewer](https://nbviewer.org/gist/nmstreethran/6afcd31bfe1c328d05056d031d1ba8f5/hiresireland.ipynb)
***EURO-CORDEX***
EURO-CORDEX data for Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/6afcd31bfe1c328d05056d031d1ba8f5/eurocordex-ie.ipynb)
Loading EURO-CORDEX data using intake-esm | [nbviewer](https://nbviewer.org/gist/nmstreethran/6afcd31bfe1c328d05056d031d1ba8f5/eurocordex-intake.ipynb)
***Grass growth***
ModVege grass growth model (Jouven et al. 2006) | [nbviewer](https://nbviewer.org/gist/nmstreethran/6afcd31bfe1c328d05056d031d1ba8f5/modvege.ipynb)
GrassCheck NI | [nbviewer](https://nbviewer.org/gist/nmstreethran/6afcd31bfe1c328d05056d031d1ba8f5/grasscheck.ipynb)
PastureBase Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/6afcd31bfe1c328d05056d031d1ba8f5/pasturebase.ipynb)
Grass10 | [nbviewer](https://nbviewer.org/gist/nmstreethran/6afcd31bfe1c328d05056d031d1ba8f5/grass10.ipynb)
***Climatic regions***
Seasonality map from EPA phenology study by Scarrott et al. (2010) | [nbviewer](https://nbviewer.org/gist/nmstreethran/6afcd31bfe1c328d05056d031d1ba8f5/seasonality-map-epa.ipynb)
Agro-environmental regions based on February rainfall by Holden and Brereton (2004) | [nbviewer](https://nbviewer.org/gist/nmstreethran/6afcd31bfe1c328d05056d031d1ba8f5/agro-environmental-regions.ipynb)

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
