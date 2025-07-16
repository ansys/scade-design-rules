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

from typing import Set

import pytest
import scade.model.suite as suite

from ansys.scade.design_rules.modelling.no_literals import NoLiterals
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def session():
    """Unique instance of the test model NoLiterals."""
    pathname = 'tests/modelling/NoLiterals/NoLiterals.etp'
    return load_session(pathname)


def format_test_data(data: list) -> list:
    """Add an id to each data, assuming the first element is a Scade path."""
    return [pytest.param(*_, id=_[0].strip('/:=').split('/')[-1]) for _ in data]


def get_failed_ids(rule: NoLiterals, object_: suite.Object) -> Set[str]:
    # make sure the violations:
    #  1. refer to object_
    #  2. are NOK
    # and return the set of identifiers
    violations = set()
    for (o, id), (status, _) in rule.violations.items():
        assert status == _FAILED
        assert o == object_
        violations.add(id)
    return violations


@pytest.mark.parametrize(
    'path, expression, expected',
    format_test_data(
        [
            ('P::O/exceptOk=', '.right', set()),
            # patterns, where only enumeration values or literals are accepted
            ('P::O/caseOk=', '.right.parameters[2].parameters[0]', set()),
            ('P::O/caseOk=', '.right.parameters[2].parameters[1]', set()),
            # values in a sequence but not patterns
            ('P::O/iteNok=', '.right.parameters[1].parameters[0]', {'2'}),
            ('P::O/iteNok=', '.right.parameters[2].parameters[0]', {'3'}),
            # number of accumulators
            ('P::O/mapfoldOk=', '.right.modifier.parameters[1]', set()),
            ('P::O/mapfoldiOk=', '.right.modifier.parameters[1]', set()),
            ('P::O/mapfoldwOk=', '.right.modifier.parameters[1]', set()),
            ('P::O/mapfoldwiOk=', '.right.modifier.parameters[1]', set()),
            # type computed by the editor: array
            ('P::O/_L25=', '.lefts[0].type.size_expression', set()),
            ('P::O/textNok=', '.right.parameters[0]', {'3'}),
            ('P::O/textNok=', '.right.parameters[1]', {'4'}),
            # size
            ('P::O/mapfoldNok=', '.right.modifier.parameters[0]', {'2'}),
            ('P::O/mapfoldiNok=', '.right.modifier.parameters[0]', {'2'}),
            ('P::O/mapfoldwNok=', '.right.modifier.parameters[0]', {'2'}),
            ('P::O/mapfoldwiNok=', '.right.modifier.parameters[0]', {'2'}),
            # slice parameters
            ('P::O/hiddenNok=', '.right.parameters[1]', {'2'}),
            # projection parameters
            ('P::O/projOk=', '.right.parameters[1]', set()),
            ('P::O/projOk=', '.right.parameters[2]', set()),
            ('P::O/projNok=', '.right.parameters[1]', {'2'}),
            # blocks
            ('P::O/IfBlockOk:', '.expression', set()),
            ('P::O/IfBlockOk:else:', '.expression.parameters[1]', set()),
            ('P::O/WhenBlockOk:', '.when', set()),
            ('P::O/SMOk:State1:<1>:', '.condition', set()),
            ('P::O/IfBlockNok:', '.expression', {'true'}),
            ('P::O/IfBlockNok:else:', '.expression.parameters[0]', {'2'}),
            ('P::O/WhenBlockNok:', '.when', {'true'}),
            ('P::O/SMNok:State1:<1>:', '.condition', {'true'}),
            ('P::O/SMNok:State1:<1>:o=', '.right', {'2'}),
        ]
    ),
)
def test_no_literals_flows(session: suite.Session, path, expression, expected):
    model = session.model

    object_ = model.get_object_from_path(path)
    if isinstance(object_, suite.IfBlock):
        object_ = object_.if_node
    assert object_
    expression = eval('object_%s' % expression)
    assert isinstance(expression, suite.ConstValue)
    rule = NoLiterals()
    assert rule.on_start(model, parameter='false, 0, 1') == _OK
    status = rule.on_check(expression)
    assert status == _NA
    ids = get_failed_ids(rule, object_)
    assert ids == expected


@pytest.mark.parametrize(
    'path, expression, expected',
    format_test_data(
        [
            ('P::O/A_NOK', '', {'true'}),
            ('P::O/A_OK', '.parameters[0]', set()),
        ]
    ),
)
def test_no_literals_assertions(session: suite.Session, path, expression, expected):
    model = session.model

    path, name = path.split('/')
    op = model.get_object_from_path(path)
    assert op
    for assertion in op.assertions:
        if assertion.name == name:
            break
    assert assertion.name == name
    expression = eval('assertion.expression%s' % expression)
    assert isinstance(expression, suite.ConstValue)
    rule = NoLiterals()
    assert rule.on_start(model, parameter='false, 0, 1') == _OK
    status = rule.on_check(expression)
    assert status == _NA
    ids = get_failed_ids(rule, assertion)
    assert ids == expected


@pytest.mark.parametrize(
    'path, expression, expected',
    format_test_data(
        [
            ('P::O/defaultNok/', '.default', {'2'}),
            ('P::O/defaultOk/', '.default', set()),
            ('P::O/lastNok/', '.last', {'-1'}),
            ('P::O/lastOk/', '.last', set()),
            ('P::O/tableNok/', '.type.size_expression', {'3'}),
            ('P::C/', '.value', set()),
            ('P::C2/', '.value.parameters[1]', set()),
            ('P::TRUE/', '.value', set()),
            ('P::Position/', '.type.size_expression', {'3'}),
            ('P::Sized16/', '.type.size_expression', {'16'}),
            ('P::Table/', '.type.size_expression.parameters[1]', set()),
        ]
    ),
)
def test_no_literals_declarations(session: suite.Session, path, expression, expected):
    model = session.model

    declaration = model.get_object_from_path(path)
    assert declaration
    expression = eval('declaration%s' % expression)
    assert isinstance(expression, suite.ConstValue)
    rule = NoLiterals()
    assert rule.on_start(model, parameter='false, 0, 1') == _OK
    status = rule.on_check(expression)
    assert status == _NA
    ids = get_failed_ids(rule, declaration)
    assert ids == expected
