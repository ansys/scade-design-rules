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

from ansys.scade.design_rules.modelling.scope_of_locals import ScopeOfLocals
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def session():
    """Unique instance of the test model ScopeOfLocals."""
    pathname = 'tests/modelling/ScopeOfLocals/ScopeOfLocals.etp'
    return load_session(pathname)


@pytest.mark.parametrize(
    'test_case',
    [
        ('P::O/SM1:State1:SM2:State11:locOk/', _OK),
        ('P::O/SM1:State1:SM2:State12:locOk/', _OK),
        ('P::O/SM1:State1:signalOk/', _OK),
        ('P::O/SM3:State31:weakOk/', _OK),
        ('P::O/SM3:State32:weakOk/', _OK),
        ('P::O/signalNok/', _FAILED),
        ('P::O/topOk/', _OK),
        ('P::O/topState1Nok/', _FAILED),
        ('P::O/topSiblingOk/', _OK),
        ('P::O/topSiblingNok/', _FAILED),
        ('P::O/topNok/', _FAILED),
        ('P::O/topUnusedOk/', _OK),
        ('P::O/weakNok/', _FAILED),
        ('P::O/strongOk/', _OK),
        ('P::O/oOK/', _NA),
        ('P::O/iOK/', _NA),
    ],
)
def test_scope_of_locals(session: suite.Session, test_case):
    path, expected_status = test_case
    model = session.model

    var = model.get_object_from_path(path)
    assert var
    rule = ScopeOfLocals()
    # assert rule.on_start(model) == _OK
    status = rule.on_check(var)
    assert status == expected_status
