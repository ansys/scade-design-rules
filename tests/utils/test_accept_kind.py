# -*- coding: utf-8 -*-

# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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


import _scade_api
import pytest
import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import SCK, Rule
from tests.conftest import load_session


# use Names.etp since it contains all the possible instances of SCADE elements
@pytest.fixture(scope='session')
def session() -> suite.Session:
    # unique model for these tests
    session = load_session('tests/naming/Names/Names.etp')
    return session


@pytest.mark.parametrize(
    'test_case',
    [
        ('', [], SCK.MODEL),
        ('Elements::Success::', [], SCK.PACKAGE),
        ('Elements::Success::Enumeration/', [], SCK.TYPE),
        ('Elements::Success::Operator/', [("'T", 'typevar')], SCK.GENERIC_TYPE),
        ('Elements::Success::Structure/', [(None, 'type'), ('field', 'element')], SCK.FIELD),
        ('Elements::Success::mySensor/', [], SCK.SENSOR),
        ('Elements::Success::CONSTANT/', [], SCK.CONSTANT),
        ('Elements::Success::VALUE/', [], SCK.ENUM_VALUE),
        ('Elements::Success::Operator/', [('N', 'parameter')], SCK.PARAMETER),
        ('Elements::Success::Operator/input/', [], SCK.INPUT),
        ('Elements::Success::Operator/hidden/', [], SCK.HIDDEN),
        ('Elements::Success::Operator/output/', [], SCK.OUTPUT),
        ('Elements::Success::Operator/local/', [], SCK.VARIABLE),
        ('Elements::Success::Operator/debug/', [], SCK.VARIABLE),
        ('Elements::Success::Operator/event/', [], SCK.SIGNAL),
        ('Elements::Success::Operator/_L1/', [], SCK.INTERNAL),
        ('Elements::Success::Operator/', [('Operator', 'diagram')], SCK.DIAGRAM),
        (
            'Elements::Success::Operator/',
            [('Operator', 'diagram'), ('My_Awful Equation set', 'equationSet')],
            SCK.EQ_SET,
        ),
        ('Elements::Success::Operator/SM1:', [], SCK.STATE_MACHINE),
        ('Elements::Success::Operator/SM1:State1:', [], SCK.STATE),
        ('Elements::Success::Operator/IfBlock1:', [], SCK.IF_BLOCK),
        ('Elements::Success::Operator/WhenBlock1:', [], SCK.WHEN_BLOCK),
    ],
)
def test_accept_kind(session: suite.Session, test_case):
    path, subpaths, expected = test_case
    model = session.model
    object_ = model.get_object_from_path(path)
    assert object_ is not None
    for name, role in subpaths:
        if name:
            object_ = {element.name: element for element in _scade_api.get(object_, role)}[name]
        else:
            object_ = _scade_api.get(object_, role)
        assert object_ is not None

    # empty rule
    rule = Rule('', '', '', 0, None)
    # loop on kinds
    for kind in SCK:
        rule.kinds = [kind]
        assert rule.accept_kind(object_) == (kind == expected)
