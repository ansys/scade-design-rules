# -*- coding: utf-8 -*-

# Copyright (C) 2021 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pathlib import Path
from shutil import rmtree
from typing import Tuple

import pytest

# shall modify sys.path to access SCACE APIs
import ansys.scade.apitools  # noqa: F401

# isort: split

from scade import load_project
import scade.model.project.stdproject as std
import scade.model.suite as suite

# ---------------------------------------------------------------------------
# utilities
# ---------------------------------------------------------------------------


def load_session(pathname: str) -> suite.Session:
    session = suite.Session()
    session.load2(pathname)
    return session


# ---------------------------------------------------------------------------
# local_tmpdir
# ---------------------------------------------------------------------------


@pytest.fixture(scope='session')
def local_tmpdir() -> Path:
    path = Path('tests') / 'tmp'
    try:
        rmtree(str(path))
    except FileNotFoundError:
        pass
    path.mkdir()
    return path


# ---------------------------------------------------------------------------
# on-the-fly models
# ---------------------------------------------------------------------------


@pytest.fixture(scope='session')
def project_session(request) -> Tuple[std.Project, suite.Session]:
    # load request.param
    assert Path(request.param).exists()
    project = load_project(request.param)
    session = load_session(request.param)
    session.model.project = project
    return (project, session)


# ---------------------------------------------------------------------------
# end of file
# ---------------------------------------------------------------------------
