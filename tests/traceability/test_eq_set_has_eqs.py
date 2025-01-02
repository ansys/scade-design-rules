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

from ansys.scade.design_rules.traceability.eq_set_has_eqs import EqSetHasEqs
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
    """Unique instance of the test model EqSetHasEqs."""
    pathname = 'tests/traceability/EqSetHasEqs/EqSetHasEqs.etp'
    return load_session(pathname)


@pytest.mark.parametrize(
    'test_case',
    [
        ('P::Operator/Correct/Flows/', _OK),
        ('P::Operator/Correct/Branch1/', _OK),
        ('P::Operator/Correct/Branch2/', _OK),
        ('P::Operator/Activate/IfBlock/', _FAILED),
        ('P::Operator/Activate/Action/', _FAILED),
        ('P::Operator/Activate/WhenBlock/', _FAILED),
        ('P::Operator/StateMachine/Machine/', _FAILED),
        ('P::Operator/StateMachine/State/', _FAILED),
    ],
)
def test_eq_set_has_eqs_nominal(session: suite.Session, test_case):
    path, expected = test_case
    model = session.model

    eqset = get_equation_set_or_diagram_from_path(model, path)
    assert eqset is not None
    rule = EqSetHasEqs()
    status = rule.on_check(eqset)
    assert status == expected
