# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys

sys.path.append("..")

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "ClimAg"
copyright = "2022-2025, Nithiya Streethran"
author = "Nithiya Streethran"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "myst_nb",
]

# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = [
    "amsmath",
    "dollarmath",
]

# disable sorting of functions by alphabetical order
autodoc_member_order = "bysource"

# do not execute Jupyter notebooks
nb_execution_mode = "off"

viewcode_line_numbers = True

# templates_path = ["_templates"]

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".ipynb_checkpoints",
    ".pytest_cache",
    "__pycache__",
    ".coverage",
    "environment.yml",
    "convert-notebooks.sh",
    ".gitignore",
    "README.md",
    "LICENCE.txt",
    "requirements.txt",
    ".readthedocs.yaml",
    "other",
    "results",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"

# html_static_path = ["_static"]

html_theme_options = {
    "icon_links": [
        {
            # Label for this link
            "name": "GitHub",
            # URL where the link will redirect
            "url": "https://github.com/ClimAg/ClimAg",  # required
            # Icon class (if 'type': 'fontawesome'), or path to local image
            # (if 'type': 'local')
            "icon": "fa-brands fa-github",
            # The type of image to be used (see below for details)
            "type": "fontawesome",
        }
    ],
    "navbar_align": "right",
}
