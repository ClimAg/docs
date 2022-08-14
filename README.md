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
ireland-boundary-nuts | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/ireland-boundary-nuts.ipynb)
ireland-boundary | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/ireland-boundary.ipynb)
clc-2018 | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/clc-2018.ipynb)

### Notebooks for the [climate-change-droughts](https://github.com/ClimAg/climate-change-droughts) project

Notebook | Link
--- | ---
eurocordex-find-icell | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/eurocordex-find-icell.ipynb)
eurocordex-process-spi-hist | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/eurocordex-process-spi-hist.ipynb)
eurocordex-process-spi-future | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/eurocordex-process-spi-future.ipynb)
eurocordex-process-spei-hist | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/eurocordex-process-spei-hist.ipynb)
eurocordex-process-spei-future | [nbviewer](https://nbviewer.org/gist/nmstreethran/20d0fdcb9fd282703aa24abd401bb8e1/eurocordex-process-spi-future.ipynb)

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
