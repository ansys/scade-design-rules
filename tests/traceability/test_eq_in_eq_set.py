# -*- coding: utf-8 -*-

# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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

from ansys.scade.design_rules.traceability.eq_in_eq_set import EqInEqSet
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def session():
    """Unique instance of the test model EqInEqSet."""
    pathname = 'tests/traceability/EqInEqSet/EqInEqSet.etp'
    return load_session(pathname)


@pytest.mark.parametrize(
    'test_case',
    [
        ('P::Equations/ok1=', _OK),
        ('P::Equations/textualOutput=', _OK),
        ('P::Equations/SM1:Embedded:ok3=', _OK),
        ('P::Equations/SM1:Embedded:inEqSet=', _OK),
        ('P::Equations/SM1:Embedded:<1.1>:forked=', _OK),
        ('P::Equations/SM1:Embedded:<1>:signal=', _OK),
        ('P::Equations/SM1:Hidden:textualLocal1=', _OK),
        ('P::Equations/SM1:Hidden:localNok1=', _FAILED),
        ('P::Equations/SM1:Hidden:localOk1=', _OK),
        ('P::Equations/SM1:Textual:ok4=', _OK),
        ('P::Equations/ok2=', _OK),
        ('P::Equations/nok1=', _FAILED),
        ('P::Equations/IfBlock1:else:else:localOk2=', _OK),
        ('P::Equations/IfBlock1:else:else:localNok2=', _FAILED),
        ('P::Equations/IfBlock1:else:else:textualLocal2=', _OK),
        ('P::Equations/IfBlock1:else:then:ok6=', _OK),
        ('P::Equations/IfBlock1:then:ok5=', _OK),
        ('P::Equations/IfBlock1:then:nok3=', _FAILED),
        ('P::Equations/nok2=', _FAILED),
        ('P::Equations/WhenBlock1:a:ok7=', _OK),
        ('P::Equations/WhenBlock1:a:nok4=', _FAILED),
        ('P::Equations/WhenBlock1:b:ok8=', _OK),
        ('P::Equations/WhenBlock1:c:textualLocal3=', _OK),
        ('P::Equations/WhenBlock1:c:localNok3=', _FAILED),
        ('P::Equations/WhenBlock1:c:localOk3=', _OK),
    ],
)
def test_eq_in_eq_set_nominal(session: suite.Session, test_case):
    path, expected = test_case
    model = session.model

    eq = model.get_object_from_path(path)
    assert eq is not None
    rule = EqInEqSet()
    status = rule.on_check(eq)
    assert status == expected


@pytest.mark.parametrize(
    'test_case',
    [
        ('P::BranchesOk/IfBlock1:else:else:else:', _OK),
        ('P::BranchesOk/IfBlock1:else:else:then:', _OK),
        ('P::BranchesOk/IfBlock1:else:then:', _OK),
        ('P::BranchesOk/IfBlock1:then:else:', _OK),
        ('P::BranchesOk/IfBlock1:then:then:', _OK),
        ('P::BranchesOk/WhenBlock1:a:', _OK),
        ('P::BranchesOk/WhenBlock1:b:', _OK),
        ('P::BranchesOk/WhenBlock1:c:', _OK),
        ('P::BranchesOk/IfBlock2:else:else:else:', _OK),
        ('P::BranchesOk/IfBlock2:else:else:then:', _OK),
        ('P::BranchesOk/IfBlock2:else:then:', _OK),
        ('P::BranchesOk/IfBlock2:then:else:', _OK),
        ('P::BranchesOk/IfBlock2:then:then:', _OK),
        ('P::BranchesOk/WhenBlock2:a:', _OK),
        ('P::BranchesOk/WhenBlock2:b:', _OK),
        ('P::BranchesOk/WhenBlock2:c:', _OK),
        ('P::BranchesStateOk/SM1:State1:IfBlock1:else:else:else:', _OK),
        ('P::BranchesStateOk/SM1:State1:IfBlock1:else:else:then:', _OK),
        ('P::BranchesStateOk/SM1:State1:IfBlock1:else:then:', _OK),
        ('P::BranchesStateOk/SM1:State1:IfBlock1:then:else:', _OK),
        ('P::BranchesStateOk/SM1:State1:IfBlock1:then:then:', _OK),
        ('P::BranchesStateOk/SM1:State1:WhenBlock1:a:', _OK),
        ('P::BranchesStateOk/SM1:State1:WhenBlock1:b:', _OK),
        ('P::BranchesStateOk/SM1:State1:WhenBlock1:c:', _OK),
        ('P::BranchesNok/IfBlock1:else:else:else:', _FAILED),
        ('P::BranchesNok/IfBlock1:else:else:then:', _FAILED),
        ('P::BranchesNok/IfBlock1:else:then:', _FAILED),
        ('P::BranchesNok/IfBlock1:then:else:', _FAILED),
        ('P::BranchesNok/IfBlock1:then:then:', _FAILED),
        ('P::BranchesNok/WhenBlock1:a:', _FAILED),
        ('P::BranchesNok/WhenBlock1:b:', _FAILED),
        ('P::BranchesNok/WhenBlock1:c:', _FAILED),
    ],
)
def test_branch_in_eq_set_nominal(session: suite.Session, test_case):
    path, expected = test_case
    model = session.model

    branch = model.get_object_from_path(path)
    if isinstance(branch, suite.IfAction):
        branch = branch.owner
    assert branch is not None
    rule = EqInEqSet()
    status = rule.on_check(branch)
    assert status == expected
