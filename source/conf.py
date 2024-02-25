# Configuration file for the Sphinx documentation builder.
#

import os
import sys

sys.path.insert(0, os.path.abspath('../Engine'))
sys.path.insert(0, os.path.abspath('../Engine/Elements'))
sys.path.insert(0, os.path.abspath('../Engine/Materials'))
sys.path.insert(0, os.path.abspath('../Pre'))
sys.path.insert(0, os.path.abspath('../Pos'))

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


project = 'FEM Project'
copyright = '2024, Lucas Lino and Christian Oliveira'
author = 'Lucas Lino and Christian Oliveira'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.todo',
              'sphinx.ext.viewcode',
              'autodocsumm']

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

autodoc_default_options = {
    'autosummary': True,
}
