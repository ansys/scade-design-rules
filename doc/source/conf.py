"""Sphinx documentation configuration file."""

from datetime import datetime
import os
from pathlib import Path
import sys

from ansys_sphinx_theme import (
    ansys_favicon,
    get_version_match,
)

from ansys.scade.design_rules import __version__

sys.path.append(str(Path('./_ext').resolve()))

# Project information
project = 'ansys-scade-design-rules'
copyright = f'(c) {datetime.now().year} ANSYS, Inc. All rights reserved'
author = 'ANSYS, Inc.'
release = version = __version__
switcher_version = get_version_match(version)

# Select desired logo, theme, and declare the html title
html_theme = 'ansys_sphinx_theme'
html_short_title = html_title = 'scade-design-rules'

# multi-version documentation
cname = os.getenv('DOCUMENTATION_CNAME', 'design-rules.scade.docs.pyansys.com')
"""The canonical name of the webpage hosting the documentation."""

# specify the location of your github repo
html_theme_options = {
    'github_url': 'https://github.com/ansys/scade-design-rules',
    'show_prev_next': False,
    'show_breadcrumbs': True,
    'additional_breadcrumbs': [
        ('PyAnsys', 'https://docs.pyansys.com/'),
    ],
    'switcher': {
        'json_url': f'https://{cname}/versions.json',
        'version_match': switcher_version,
    },
    'check_switcher': False,
    'logo': 'pyansys',
}

# Sphinx extensions
extensions = [
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
    'sphinx_design',
    'sdr',
]

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3.11', None),
    # kept here as an example
    # "scipy": ("https://docs.scipy.org/doc/scipy/reference", None),
    # "numpy": ("https://numpy.org/devdocs", None),
    # "matplotlib": ("https://matplotlib.org/stable", None),
    # "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    # "pyvista": ("https://docs.pyvista.org/", None),
    # "grpc": ("https://grpc.github.io/grpc/python/", None),
}

# Favicon
html_favicon = ansys_favicon

# static path
html_static_path = ['_static']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# TODO: remove ignore links after public release
linkcheck_ignore = [
    'https://github.com/ansys/scade-design-rules',
    'https://github.com/ansys/scade-design-rules/actions/workflows/ci_cd.yml',
    'https://pypi.org/project/ansys-scade-design-rules',
    # The link below takes a long time to check
    'https://www.ansys.com/products/embedded-software/ansys-scade-suite',
    'https://www.ansys.com/*',
]


if switcher_version != 'dev':
    linkcheck_ignore.append(
        f'https://github.com/ansys/scade-design-rules/releases/tag/v{__version__}'
    )

# Common content for every RST file such us links
rst_epilog = ''
links_filepath = Path(__file__).parent.absolute() / 'links.rst'
rst_epilog += links_filepath.read_text(encoding='utf-8')

# Directories excluded when looking for source files
exclude_patterns = ['links.rst']

# Ignore checking SCADE user manual link
linkcheck_ignore = [
    r'https://ansyshelp.ansys.com/public/Views/Secured/SCADE/.+',
    r'https://github.com/ansys/scade-design-rules/issues',
    r'https://github.com/ansys/scade-design-rules/pull/.*',
]
