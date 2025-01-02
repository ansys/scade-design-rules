# -*- coding: utf-8 -*-

# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

import pytest
import scade.model.suite as suite

from ansys.scade.design_rules.project_structure.no_scade_library import NoScadeLibrary
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def session():
    """Unique instance of the test model Project."""
    pathname = 'tests/project_structure/Libraries/Models/Project/Project.etp'
    return load_session(pathname, project=pathname)


@pytest.mark.parametrize(
    'test_case',
    [
        ('Project', 0, {'libpwlinear.etp', 'Library.etp', 'Module1.etp'}, _FAILED),
        ('Module1', 0, {'Module2.etp'}, _FAILED),
        ('Module2', 0, {'libdigital.etp'}, _FAILED),
        ('Library', 0, set(), _OK),
        ('Project', 1, {'libpwlinear.etp', 'Library.etp'}, _FAILED),
        ('Module1', 1, set(), _OK),
        ('Module2', 1, {'libdigital.etp'}, _FAILED),
        ('Library', 1, set(), _OK),
        ('Project', 2, {'libpwlinear.etp'}, _FAILED),
        ('Module1', 2, set(), _OK),
        ('Module2', 2, {'libdigital.etp'}, _FAILED),
        ('Library', 2, set(), _OK),
    ],
)
def test_no_scade_library(session: suite.Session, test_case):
    name, upper_levels, expected_failures, expected_status = test_case
    model = session.model

    library = {library.name: library for library in model.session.loaded_models}[name]
    assert library is not None
    rule = NoScadeLibrary()
    parameter = 'upper_levels=%d' % upper_levels
    assert rule.on_start(model, parameter) == _OK
    status = rule.on_check(library, parameter)
    assert status == expected_status
    failures = {Path(path).name for path in rule.message.split('\n')[1:]}
    assert failures == expected_failures
