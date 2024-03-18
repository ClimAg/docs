# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys

sys.path.append("..")

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "ClimAg"
copyright = "2022-2024, Nithiya Streethran"
author = "Nithiya Streethran"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "myst_nb",
    "sphinx.ext.intersphinx",
]

# https://docs.readthedocs.io/en/stable/guides/intersphinx.html
# We recommend adding the following config value.
# Sphinx defaults to automatically resolve *unresolved* labels using all your Intersphinx mappings.
# This behavior has unintended side-effects, namely that documentations local references can
# suddenly resolve to an external location.
# See also:
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#confval-intersphinx_disabled_reftypes
intersphinx_disabled_reftypes = ["*"]

intersphinx_mapping = {
    "climag": ("https://climag.readthedocs.io/", "objects.inv"),
}

# disable sorting of functions by alphabetical order
autodoc_member_order = "bysource"

# do not execute Jupyter notebooks
nb_execution_mode = "off"

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
            "url": "https://github.com/ClimAg",  # required
            # Icon class (if 'type': 'fontawesome'), or path to local image
            # (if 'type': 'local')
            "icon": "fa-brands fa-github",
            # The type of image to be used (see below for details)
            "type": "fontawesome",
        }
    ],
    "navbar_align": "right",
}
