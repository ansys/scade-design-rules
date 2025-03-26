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

from ansys.scade.design_rules.readability.local_name_uniqueness import LocalNameUniqueness
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def session():
    """Unique instance of the test model LocalNameUniqueness."""
    pathname = 'tests/readability/LocalNameUniqueness/LocalNameUniqueness.etp'
    return load_session(pathname)


@pytest.mark.parametrize(
    'test_case',
    [
        ('P::Function/speed/', _OK),
        ('P::Function/status/', _OK),
        ('P::Node/SM1:State1:sibling/', _FAILED),
        ('P::Node/SM1:State1:state1/', _OK),
        ('P::Node/SM1:State2:sibling/', _FAILED),
        ('P::Node/SM1:State2:state2/', _OK),
        ('P::Node/IfBlock1:else:SM2:State3:sibling/', _FAILED),
        ('P::Node/IfBlock1:else:SM2:State3:override/', _FAILED),
        ('P::Node/IfBlock1:else:SM2:State3:override2/', _FAILED),
        ('P::Node/IfBlock1:else:override2/', _FAILED),
        ('P::Node/IfBlock1:then:override/', _FAILED),
        ('P::Node/status/', _OK),
        ('P::Node/speed/', _OK),
        ('P::Node/override/', _FAILED),
    ],
)
def test_local_name_uniqueness_nominal(session: suite.Session, test_case):
    path, expected = test_case
    model = session.model

    variable = model.get_object_from_path(path)
    assert variable is not None
    operator = model.get_object_from_path(path.split('/')[0])
    assert operator is not None
    rule = LocalNameUniqueness()
    status = rule.before_checking_subtree(operator)
    assert status == _OK
    status = rule.before_checking_subtree(variable)
    assert status == _OK
    status = rule.on_check(operator)
    assert status == _OK
    status = rule.on_check(variable)
    assert status == expected
