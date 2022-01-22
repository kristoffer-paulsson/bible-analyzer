import sys, os
from bibleanalyzer.data import NAME, VERSION

sys.path.insert(0, os.path.abspath('../src/'))

project = NAME
copyright = '2021, Kristoffer Paulsson'
author = 'Kristoffer Paulsson'

# The full version, including alpha/beta/rc tags
release = VERSION

extensions = [
    "recommonmark",  # Markdown support
    "sphinx.ext.napoleon",  #
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
]

templates_path = ['_templates']
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]