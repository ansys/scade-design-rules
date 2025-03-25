# -*- coding: utf-8 -*-

# Copyright (C) 2024 - 2025 ANSYS, Inc. and/or its affiliates.
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

from typing import Any, Tuple

import pytest
from scade.model.project.stdproject import Project
import scade.model.suite as suite

from ansys.scade.design_rules.traceability.llr_only_eqs import LLROnlyEqs
from ansys.scade.design_rules.utils.rule import Rule
from tests.utils.utils import get_equation_set_or_diagram_from_path, get_project_requirement_ids

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


# the requirements are not available for the projects loaded
# with conftest.py (fixtures project_session_trace)
class TestLLROnlyEqs(LLROnlyEqs):
    __test__ = False

    def __init__(self, links):
        super().__init__()
        self.links = links

    def get_requirement_ids(self, traceable: suite.Traceable):
        return self.links.get(traceable.get_oid(), [])


@pytest.mark.parametrize(
    'project_session_trace', ['tests/traceability/LLROnly/LLROnly.etp'], indirect=True
)
@pytest.mark.parametrize(
    'test_case',
    [
        ('P::O/', _FAILED),
        ('P::O/IfBlock1:', _FAILED),
        ('P::O/IfBlock1:else:', _FAILED),
        ('P::O/SM1:', _FAILED),
        ('P::O/SM1:State1:<1>:', _FAILED),
        ('P::O/SM1:State1:<1.1>:', _FAILED),
        ('P::O/SM1:State1:<2>:', _FAILED),
        ('P::O/SM1:State3:', _FAILED),
        ('P::O/Graphical/EquationSet1/', _OK),
        ('P::O/Textual/', _OK),
        ('P::O/o/', _FAILED),
    ],
)
def test_llr_only_eqs_nominal(project_session_trace: Tuple[Project, suite.Session, Any], test_case):
    project, session, trace = project_session_trace
    path, expected = test_case
    model = session.model

    traceable = model.get_object_from_path(path)
    if not traceable:
        traceable = get_equation_set_or_diagram_from_path(model, path)
    # API not consistent
    if isinstance(traceable, suite.IfAction):
        traceable = traceable.action
    assert traceable is not None
    print(str(traceable))
    rule = TestLLROnlyEqs(get_project_requirement_ids(trace))
    status = rule.on_check(traceable)
    assert status == expected
