# jupyter-notebooks

[ClimAg](https://www.ucc.ie/en/eel/projects/climag/): Multifactorial causes of
fodder crises in Ireland and risks due to climate change

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
