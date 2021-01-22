# -*- coding: utf-8 -*-

import os
import sys
import time

# -- Path setup ------------------------------------------------------------------------

sys.path.insert(0, os.path.abspath("../src"))

# -- Project information ---------------------------------------------------------------

author = "Sam Schott"
version = "1.1.2"
release = version
project = "dekstop-notifier"
title = "Desktop-Notifier Documentation"
copyright = "{}, {}".format(time.localtime().tm_year, author)

# -- General configuration -------------------------------------------------------------

extensions = [
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "autoapi.extension",
    "m2r2",
]
source_suffix = [".rst", ".md"]
master_doc = "index"
language = "en"
# html4_writer = True

# -- Options for HTML output -----------------------------------------------------------

html_theme = "sphinx_rtd_theme"

# -- Extension configuration -----------------------------------------------------------

# sphinx.ext.autodoc
autodoc_typehints = "description"

# autoapi.extension
autoapi_type = "python"
autoapi_dirs = ["../src/desktop_notifier"]
autoapi_options = [
    "members",
    "show-inheritance",
    "show-module-summary",
    "undoc-members",
]
autoapi_add_toctree_entry = False

# sphinx.ext.todo
todo_include_todos = True

# sphinx.ext.intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}
