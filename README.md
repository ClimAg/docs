# ClimAg docs

[![Documentation Status](https://readthedocs.org/projects/climag/badge/?version=latest)](https://climag.readthedocs.io/?badge=latest)

Documentation and Jupyter notebooks for the ClimAg research project.
Available at: <https://climag.readthedocs.io>.

ClimAg is a three-year research project funded by the [Environmental Protection Agency (EPA)](https://www.epa.ie/) under the Climate Change Research Programme grant number 2018-CCRP-MS.50, with additional funding provided under the COVID-19 research support scheme of the [Higher Education Authority](https://hea.ie/).

## Installation

This project uses [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) with [Python](https://www.python.org/) 3.10.
Windows users should use Conda within [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install), as some packages (e.g. [CDO](https://code.mpimet.mpg.de/projects/cdo)) are unavailable for Windows.

Clone the ClimAg repository including submodules:

```sh
git clone --recurse-submodules https://github.com/ClimAg/ClimAg.git
cd ClimAg
```

Create a virtual environment and install all requirements:

```sh
conda env create
```

Activate the virtual environment:

```sh
conda activate ClimAg
```

To run tests:

```sh
python -m pytest
```

To generate a coverage report with the tests:

```sh
coverage run -m pytest && coverage report -m
```

To update the virtual environment:

```sh
conda env update
```

## Licence

Copyright 2022-2024 N. Streethran

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  <https://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
