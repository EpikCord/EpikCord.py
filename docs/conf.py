import os
import sys

sys.path.insert(0, os.path.abspath("../EpikCord"))
project = "EpikCord.py"
copyright = "2022, EpikCord"
author = "EpikCord"

release = "0.4.13"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

napoleon_google_docstring = False
napoleon_use_param = False

templates_path = ["_templates"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


html_theme = "sphinx_rtd_theme"

html_static_path = ["_static"]
master_doc = "index"
