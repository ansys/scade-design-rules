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

from ansys.scade.design_rules.naming.name_structure_iterator_continue import (
    NameStructureIteratorContinue,
)
from tests.conftest import load_session

# shorter names
_OK = NameStructureIteratorContinue.OK
_FAILED = NameStructureIteratorContinue.FAILED
_ERROR = NameStructureIteratorContinue.ERROR
_NA = NameStructureIteratorContinue.NA


@pytest.fixture(scope='session')
def session() -> suite.Session:
    # unique model for these tests
    session = load_session('tests/naming/NameStructureIterators/NameStructureIterators.etp')
    return session


@pytest.mark.parametrize(
    'test_case',
    [
        (2, 'continue', _OK),
        (2, 'notContinue', _FAILED),
    ],
)
def test_name_structure_iterator_continue_nominal(session: suite.Session, test_case):
    index, name, expected = test_case
    model = session.model

    operator = model.get_object_from_path('P::MapFoldwi/')
    assert operator is not None
    parameter = 'continue= continue'
    rule = NameStructureIteratorContinue()
    variable = (operator.inputs + operator.hiddens + operator.outputs)[index]
    backup = variable.name
    assert rule.on_start(model, parameter) == _OK
    variable.name = name
    status = rule.on_check(variable, parameter)
    variable.name = backup
    assert status == expected


@pytest.mark.parametrize(
    'test_case',
    [
        ('P::Operator/_L1/', _NA),
        ('P::Operator/local/', _NA),
        ('P::Operator/accIn/', _NA),
        ('P::Operator/index/', _NA),
        ('P::Operator/accValueOut/', _OK),
    ],
)
def test_name_structure_iterator_continue_n_a(session: suite.Session, test_case):
    path, expected = test_case
    model = session.model

    variable = model.get_object_from_path(path)
    assert variable is not None
    parameter = '-c continue'
    rule = NameStructureIteratorContinue()
    assert rule.on_start(model, parameter) == _OK
    assert rule.on_check(variable, parameter) == expected


@pytest.mark.parametrize(
    'test_case',
    [
        ('a, b', _ERROR),
        ('not_continue=abcd', _ERROR),
        ('continue=abcd', _OK),
        ('--continue abcd', _OK),
        ('-c abcd', _OK),
    ],
)
def test_name_structure_fold_accumulator_parameter(test_case):
    parameter, expected = test_case

    rule = NameStructureIteratorContinue()
    assert rule.on_start(suite.Model(), parameter) == expected
