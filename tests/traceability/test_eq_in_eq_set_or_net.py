# -*- coding: utf-8 -*-

# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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

from ansys.scade.design_rules.traceability.eq_in_eq_set_or_net import EqInEqSetOrNet
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def session():
    """Unique instance of the test model EqInEqSetOrNet."""
    pathname = 'tests/traceability/EqInEqSetOrNet/EqInEqSetOrNet.etp'
    return load_session(pathname)


@pytest.mark.parametrize(
    'test_case',
    [
        ('P::Operator/ok1=', _OK),
        ('P::Operator/nok1=', _FAILED),
        ('P::Operator/ok2=', _OK),
        ('P::Operator/SM1:State1:ok3=', _OK),
        ('P::Operator/nok2=', _FAILED),
    ],
)
def test_eq_in_eq_set_or_net_nominal(session: suite.Session, test_case):
    path, expected = test_case
    model = session.model

    eq = model.get_object_from_path(path)
    assert eq is not None
    rule = EqInEqSetOrNet()
    status = rule.on_check(eq)
    assert status == expected
