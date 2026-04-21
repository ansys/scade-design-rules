# -*- coding: utf-8 -*-

# Copyright (C) 2024 - 2026 ANSYS, Inc. and/or its affiliates.
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
import sys

# shall modify sys.path to access SCACE APIs
import ansys.scade.apitools  # noqa: F401

# isort: split

import pytest
import scade
import scade.model.project.stdproject as std
import scade.model.suite as suite

from ansys.scade.apitools.info import get_scade_version

sys.path.append(str(Path(__file__).parent.parent))


def load_session(*paths: str, project: str = '') -> suite.Session:
    """
    Create an instance of Session instance and load the requested models.
    """
    session = suite.Session()
    for path in paths:
        session.load2(path)
    if project:
        session.model.project = load_project(project)
    return session


def load_project(path: str) -> std.Project:
    """
    Load a Scade project in a separate environment.

    Note: Undocumented API.
    """
    project = scade.load_project(str(path))
    return project


def filter_stderr(stderr: str) -> str:
    """Filter coverage warnings from ``pytest-cov``."""
    if get_scade_version() <= 231:
        text = '\n'.join(
            [
                _
                for _ in stderr.split('\n')
                if 'CoverageWarning' not in _ and 'real_section, unknown, filename' not in _
            ]
        )
    else:
        text = stderr
    return text


# on-the-fly models with traceability (2023 R1 and later)
@pytest.fixture(scope='session')
def project_session_trace(request):
    # default
    # load request.param
    project = load_project(request.param)
    session = load_session(request.param)
    # load traceability
    try:
        from scade.model.traceability.traceability import AlmgrParser, load

        # quick and dirty/ugly/smart hack:
        # the almgr files used for the tests are compatible for the considered versions of SCADE
        # so let's hack the API so that they can be loaded either with 2023 R1 or 2023 R2
        AlmgrParser.XML_NS['scade_req'] = (
            'http://www.ansys.com/scade/lifecycle/almgateway/scade_req/3'
        )
        AlmgrParser.PROJECT = f'{{{AlmgrParser.XML_NS["scade_req"]}}}ReqProject'

        trace = load(request.param)
    except BaseException:
        trace = None
    return (project, session, trace)
