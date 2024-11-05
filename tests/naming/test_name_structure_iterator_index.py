# -*- coding: utf-8 -*-

# Copyright (C) 2021 - 2024 ANSYS, Inc. and/or its affiliates.
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

from ansys.scade.design_rules.naming.name_structure_iterator_index import (
    NameStructureIteratorIndex,
)
from tests.conftest import load_session

# shorter names
_OK = NameStructureIteratorIndex.OK
_FAILED = NameStructureIteratorIndex.FAILED
_ERROR = NameStructureIteratorIndex.ERROR
_NA = NameStructureIteratorIndex.NA


@pytest.fixture(scope='session')
def session() -> suite.Session:
    # unique model for these tests
    session = load_session('tests/naming/NameStructureIterators/NameStructureIterators.etp')
    return session


@pytest.mark.parametrize(
    'test_case',
    [
        (0, 'index', _OK),
        (0, 'notIndex', _FAILED),
    ],
)
def test_name_structure_iterator_continue_nominal(session: suite.Session, test_case):
    index, name, expected = test_case
    model = session.model

    operator = model.get_object_from_path('P::MapFoldwi/')
    assert operator is not None
    parameter = '-i index'
    rule = NameStructureIteratorIndex()
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
        ('P::Operator/accIn/', _OK),
        ('P::Operator/continue/', _NA),
        ('P::Operator/accValueOut/', _NA),
    ],
)
def test_name_structure_iterator_continue_n_a(session: suite.Session, test_case):
    path, expected = test_case
    model = session.model

    variable = model.get_object_from_path(path)
    assert variable is not None
    parameter = ' --index    index '
    rule = NameStructureIteratorIndex()
    assert rule.on_start(model, parameter) == _OK
    assert rule.on_check(variable, parameter) == expected


@pytest.mark.parametrize(
    'test_case',
    [
        ('a, b', _ERROR),
        ('not_index=abcd', _ERROR),
        ('index=abcd', _OK),
        ('--index abcd', _OK),
        ('-i abcd', _OK),
    ],
)
def test_name_structure_fold_accumulator_parameter(test_case):
    parameter, expected = test_case

    rule = NameStructureIteratorIndex()
    assert rule.on_start(suite.Model(), parameter) == expected
