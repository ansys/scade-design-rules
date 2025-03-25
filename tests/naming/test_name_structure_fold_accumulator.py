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

from ansys.scade.design_rules.naming.name_structure_fold_accumulator import (
    NameStructureFoldAccumulator,
)
from tests.conftest import load_session

# shorter names
_OK = NameStructureFoldAccumulator.OK
_FAILED = NameStructureFoldAccumulator.FAILED
_ERROR = NameStructureFoldAccumulator.ERROR
_NA = NameStructureFoldAccumulator.NA


@pytest.fixture(scope='session')
def session() -> suite.Session:
    # unique model for these tests
    session = load_session('tests/naming/NameStructureIterators/NameStructureIterators.etp')
    return session


@pytest.mark.parametrize(
    'test_case',
    [
        (1, 'accIn', _OK),
        (1, 'accValueIn', _OK),
        (1, 'valueIn', _FAILED),
        (1, 'In', _FAILED),
        (1, 'accvalue', _FAILED),
        (1, 'acc', _FAILED),
        (3, 'accOut', _OK),
        (3, 'accValueOut', _OK),
        (3, 'valueOut', _FAILED),
        (3, 'Out', _FAILED),
        (3, 'accvalue', _FAILED),
        (3, 'acc', _FAILED),
    ],
)
def test_name_structure_fold_accumulator_nominal(session: suite.Session, test_case):
    index, name, expected = test_case
    model = session.model

    operator = model.get_object_from_path('P::MapFoldwi/')
    assert operator is not None
    parameter = 'in= acc.*In, out=acc.*Out'
    rule = NameStructureFoldAccumulator()
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
        (1, 'accIn', 'acc(.*)In', 'acc(.*)Out', _FAILED),
        (1, 'accIn', 'acc(.*)In', 'accVal(.*)ueOut', _OK),
        (1, 'accValueIn', 'acc(.*)In', 'acc(.*)Out', _OK),
        (3, 'accOut', 'acc(.*)In', 'acc(.*)Out', _OK),
        (3, 'accValueOut', 'acc(.*)In', 'acc(.*)Out', _FAILED),
        (3, 'accValueOut', 'acc(.*)In', 'accValue(.*)Out', _OK),
    ],
)
def test_name_structure_fold_accumulator_match(session: suite.Session, test_case):
    index, name, in_, out, expected = test_case
    model = session.model

    operator = model.get_object_from_path('P::MapFoldwi/')
    assert operator is not None
    parameter = '-i %s -o %s' % (in_, out)
    rule = NameStructureFoldAccumulator()
    variable = (operator.inputs + operator.hiddens + operator.outputs)[index]
    backup = variable.name
    assert rule.on_start(model, parameter) == _OK
    variable.name = name
    status = rule.on_check(variable, parameter)
    variable.name = backup
    if status != expected:
        print(rule.message)
    assert status == expected


def test_name_structure_fold_accumulator_no_fold(session: suite.Session):
    model = session.model

    operator = model.get_object_from_path('P::Operator/')
    assert operator is not None
    parameter = '--in acc.*In --out acc.*Out'
    rule = NameStructureFoldAccumulator()
    assert rule.on_start(model, parameter) == _OK
    assert rule.on_check(operator.inputs[1], parameter) == _OK
    assert rule.on_check(operator.outputs[1], parameter) == _OK


def test_name_structure_fold_accumulator_strict(session: suite.Session):
    model = session.model

    operator = model.get_object_from_path('P::Operator/')
    assert operator is not None
    parameter = '-i acc.*In -o acc.*Out --strict'
    rule = NameStructureFoldAccumulator()
    assert rule.on_start(model, parameter) == _OK
    assert rule.on_check(operator.inputs[1], parameter) == _FAILED
    assert rule.on_check(operator.outputs[1], parameter) == _FAILED


@pytest.mark.parametrize(
    'test_case',
    [
        ('P::Operator/_L1/', _NA),
        ('P::Operator/local/', _NA),
        ('P::Operator/index/', _OK),
        ('P::Operator/continue/', _OK),
    ],
)
def test_name_structure_fold_accumulator_n_a(session: suite.Session, test_case):
    path, expected = test_case
    model = session.model

    variable = model.get_object_from_path(path)
    assert variable is not None
    parameter = 'in=acc.*In, out= acc.*Out'
    rule = NameStructureFoldAccumulator()
    assert rule.on_start(model, parameter) == _OK
    assert rule.on_check(variable, parameter) == expected


@pytest.mark.parametrize(
    'test_case',
    [
        ('a, b', _ERROR),
        ('not_in=abcd, out=fghi', _ERROR),
        ('in=abcd, not_out=fghi', _ERROR),
        ('in=abcd, out=fghi', _OK),
        ('--in abcd --out fghi --strict', _OK),
        ('-i abcd -o fghi -s', _OK),
        ('-i abcd -o fghi', _OK),
    ],
)
def test_name_structure_fold_accumulator_parameter(test_case):
    parameter, expected = test_case

    rule = NameStructureFoldAccumulator()
    assert rule.on_start(suite.Model(), parameter) == expected
