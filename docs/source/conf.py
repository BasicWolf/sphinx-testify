import os
import sys
from pathlib import Path

sys.path.insert(0, str(
    Path(__file__).parent.resolve() / '../../src/'
))

_is_running_in_readthedocs_builder = os.environ.get('READTHEDOCS') == 'True'

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'sphinx-testify'
copyright = '2024, Zaur Nasibov'
author = 'Zaur Nasibov'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    'sphinx_testify'
]

testify_from = [
    os.path.abspath(os.path.dirname(__file__) + '/../../test_results.xml')
]

testify_skip = _is_running_in_readthedocs_builder

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
