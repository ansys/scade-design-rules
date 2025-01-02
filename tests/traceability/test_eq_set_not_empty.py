# -*- coding: utf-8 -*-

# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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


import pytest
import scade.model.suite as suite

from ansys.scade.design_rules.traceability.eq_set_not_empty import EqSetNotEmpty
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session
from tests.utils.utils import get_equation_set_or_diagram_from_path

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def session():
    """Unique instance of the test model EqSetNotEmpty."""
    pathname = 'tests/traceability/EqSetNotEmpty/EqSetNotEmpty.etp'
    return load_session(pathname)


@pytest.mark.parametrize(
    'test_case',
    [
        ('P::Operator/SM1:Hidden:Hidden_1/HiddenEmpty/', _FAILED),
        ('P::Operator/SM1:Hidden:Hidden_1/Probe/', _OK),
        ('P::Operator/Operator_1/Inputs/', _OK),
        ('P::Operator/Operator_1/Logical/', _OK),
        ('P::Operator/Operator_1/Outputs/', _OK),
        ('P::Operator/Operator_1/DataFLow/', _OK),
        ('P::Operator/Operator_1/ToplevelEmpty/', _FAILED),
        ('P::Operator/Operator_1/EmbeddedEmpty/', _FAILED),
        ('P::Operator/Operator_1/Embedded/', _OK),
    ],
)
def test_eq_set_not_empty_nominal(session: suite.Session, test_case):
    path, expected = test_case
    model = session.model

    eqset = get_equation_set_or_diagram_from_path(model, path)
    assert eqset is not None
    rule = EqSetNotEmpty()
    status = rule.on_check(eqset)
    assert status == expected
