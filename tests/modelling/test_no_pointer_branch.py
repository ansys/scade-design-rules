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

from ansys.scade.design_rules.modelling.no_pointer_branch import NoPointerBranch
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def session():
    """Unique instance of the test model NoPointerBranch."""
    pathname = 'tests/modelling/NoPointerBranch/NoPointerBranch.etp'
    return load_session(pathname)


# instantiation alias
class TestNoPointerBranch(NoPointerBranch):
    __test__ = False

    def __init__(self, parameter=None, **kwargs):
        self.parameter = parameter
        super().__init__(id='', parameter=self.parameter, **kwargs)

    def on_start(self, model=None, parameter=None):
        parameter = parameter if parameter else self.parameter
        return super().on_start(model=model, parameter=parameter)

    def on_check(self, object, parameter=None):
        parameter = parameter if parameter else self.parameter
        return super().on_check(object, parameter=parameter)


@pytest.mark.parametrize(
    'test_case',
    [
        ('P::Nominal/_L1/', _OK),
        ('P::Nominal/_L2/', _OK),
        ('P::Nominal/_L4/', _FAILED),
        ('P::Nominal/_L3/', _OK),
        ('P::Nominal/_L5/', _OK),
        ('P::Nominal/_L6/', _OK),
        ('P::Nominal/_L7/', _OK),
        ('P::Nominal/_L9/', _OK),
        ('P::Nominal/_L8/', _OK),
        ('P::Nominal/o/', _OK),
        ('P::Nominal/i1/', _OK),
        ('P::Nominal/i2/', _OK),
    ],
)
def test_no_pointer_branch(session: suite.Session, test_case):
    path, expected_status = test_case
    model = session.model

    variable = model.get_object_from_path(path)
    assert variable
    rule = TestNoPointerBranch(parameter='-t [Pp]tr.*')
    assert rule.on_start(model) == _OK
    status = rule.on_check(variable)
    assert status == expected_status


@pytest.mark.parametrize(
    'test_case',
    [
        ('', _ERROR),
        ('-t', _ERROR),
        ('--type', _ERROR),
        ('--type *Ptr', _OK),
    ],
)
def test_no_pointer_branch_robustness(test_case):
    parameter, expected_status = test_case
    rule = TestNoPointerBranch(parameter=parameter)
    status = rule.on_start()
    print(rule.message)
    assert status == expected_status
