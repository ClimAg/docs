# jupyter-notebooks

Jupyter notebooks for the [ClimAg](https://www.ucc.ie/en/eel/projects/climag/) research project

This research was funded by the Environment Protection Agency (EPA), Ireland
project "ClimAg: Multifactorial causes of fodder crises in Ireland and risks
due to climate change" under the Climate Change Research Programme grant
number 2018-CCRP-MS.50.

## Requirements

- Python 3
- JupyterLab
- Dask
- Matplotlib

## Python environment

Conda (specifications are defined in `environment.yml`):

```sh
conda env create
conda activate ClimAg
```

To update the environment:

```sh
conda env update --name ClimAg --file environment.yml
```

venv:

```sh
python3 -m venv env
source env/bin/activate
python -m pip install --upgrade pip
python -m pip install jupyterlab dask
```

## Notebooks

Notebook | Link
--- | ---
Ireland boundary - NUTS 2021 | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/ireland-boundary-nuts.ipynb)
Ireland boundary - Ordnance Survey Ireland / Northern Ireland | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/ireland-boundary.ipynb)
CORINE land cover 2018 | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/clc-2018.ipynb)

### Notebooks for the [climate-change-droughts](https://github.com/ClimAg/climate-change-droughts) project

Notebook | Link
--- | ---
Find closest EURO-CORDEX icell to study location | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/eurocordex-find-icell.ipynb)
SPI - historical - Cork Airport | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/eurocordex-process-spi-hist-ca.ipynb)
SPI - future - Cork Airport | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/eurocordex-process-spi-future-ca.ipynb)
SPEI - historical - Cork Airport | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/eurocordex-process-spei-hist-ca.ipynb)
SPEI - future - Cork Airport | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/eurocordex-process-spi-future-ca.ipynb)
SPI - historical - Moore Park | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/eurocordex-process-spi-hist.ipynb)
SPI - future - Moore Park | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/eurocordex-process-spi-future.ipynb)
SPEI - historical - Moore Park | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/eurocordex-process-spei-hist.ipynb)
SPEI - future - Moore Park | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/eurocordex-process-spi-future.ipynb)

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
