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


import pytest
import scade.model.suite as suite

from ansys.scade.design_rules.traceability.all_in_eq_set import AllInEqSet
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def session():
    """Unique instance of the test model AllInEqSet."""
    pathname = 'tests/traceability/AllInEqSet/AllInEqSet.etp'
    return load_session(pathname)


@pytest.mark.parametrize(
    'test_case',
    [
        (0, 'P::Equations/ok1=', _OK),
        (1, 'P::Equations/textualOutput=', _OK),
        (2, 'P::Equations/ok2=', _OK),
        (3, 'P::Equations/nok1=', _FAILED),
        (4, 'P::Equations/nok2=', _FAILED),
        (5, 'P::BranchesOk/IfBlock1:else:else:', _OK),
        (6, 'P::BranchesOk/IfBlock1:else:', _OK),
        (7, 'P::BranchesOk/IfBlock1:then:', _OK),
        (8, 'P::BranchesOk/IfBlock1:', _OK),
        (9, 'P::BranchesOk/WhenBlock1:a:', _OK),
        (10, 'P::BranchesOk/WhenBlock1:b:', _OK),
        (11, 'P::BranchesOk/WhenBlock1:c:', _OK),
        (12, 'P::BranchesOk/IfBlock2:else:else:', _OK),
        (13, 'P::BranchesOk/IfBlock2:else:', _OK),
        (14, 'P::BranchesOk/IfBlock2:then:', _OK),
        (15, 'P::BranchesOk/IfBlock2:', _OK),
        (16, 'P::BranchesOk/WhenBlock2:a:', _OK),
        (17, 'P::BranchesOk/WhenBlock2:b:', _OK),
        (18, 'P::BranchesOk/WhenBlock2:c:', _OK),
        (19, 'P::BranchesNok/IfBlock1:else:else:', _FAILED),
        (20, 'P::BranchesNok/IfBlock1:else:', _FAILED),
        (21, 'P::BranchesNok/IfBlock1:then:', _FAILED),
        (22, 'P::BranchesNok/IfBlock1:', _FAILED),
        (23, 'P::BranchesNok/WhenBlock1:a:', _FAILED),
        (24, 'P::BranchesNok/WhenBlock1:b:', _FAILED),
        (25, 'P::BranchesNok/WhenBlock1:c:', _FAILED),
        (26, 'P::StatesOK/SM1:Embedded:ok1=', _OK),
        (27, 'P::StatesOK/SM1:Embedded:<1.1>:forked=', _OK),
        (28, 'P::StatesOK/SM1:Embedded:<1.1>:', _OK),
        (29, 'P::StatesOK/SM1:Embedded:<1>:signal=', _OK),
        (30, 'P::StatesOK/SM1:Embedded:<1>:', _OK),
        (31, 'P::StatesOK/SM1:Embedded:', _OK),
        (32, 'P::StatesOK/SM1:Hidden:textualLocal1=', _OK),
        (33, 'P::StatesOK/SM1:Hidden:localOk1=', _OK),
        (34, 'P::StatesOK/SM1:Hidden:', _OK),
        (35, 'P::StatesOK/SM1:Textual:ok2=', _OK),
        (36, 'P::StatesOK/SM1:Textual:', _OK),
        (37, 'P::StatesNok/SM1:Embedded:nok1=', _FAILED),
        (38, 'P::StatesNok/SM1:Embedded:<1.1>:forked=', _OK),
        (39, 'P::StatesNok/SM1:Embedded:<1.1>:', _FAILED),
        (40, 'P::StatesNok/SM1:Embedded:<1>:signal=', _OK),
        (41, 'P::StatesNok/SM1:Embedded:<1>:', _FAILED),
        (42, 'P::StatesNok/SM1:Embedded:', _FAILED),
        (43, 'P::StatesNok/SM1:Hidden:localNok1=', _FAILED),
        (44, 'P::StatesNok/SM1:Hidden:', _FAILED),
        (45, 'P::StatesNok/SM1:Textual:', _FAILED),
    ],
)
def test_all_in_eq_set_nominal(session: suite.Session, test_case):
    _, path, expected = test_case
    model = session.model

    presentable = model.get_object_from_path(path)
    assert presentable is not None
    if isinstance(presentable, suite.IfBlock):
        # IfBlock and first IfNode have the same Scade path
        presentable = presentable.if_node
    rule = AllInEqSet()
    status = rule.on_check(presentable)
    assert status == expected
