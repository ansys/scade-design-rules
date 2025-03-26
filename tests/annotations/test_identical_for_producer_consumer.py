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

from ansys.scade.design_rules.annotations.identical_for_producer_consumer import (
    IdenticalForProducerConsumer,
)
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def session() -> suite.Session:
    # unique model for these tests
    session = load_session(
        'tests/annotations/IdenticalForProducerConsumer/IdenticalForProducerConsumer.etp'
    )
    return session


@pytest.mark.parametrize(
    'path, expected',
    [
        ('P::O/emptyOk/', _OK),
        ('P::O/definedOk/', _OK),
        ('P::O/predefNa/', _OK),
        ('P::O/unitNok/', _FAILED),
        ('P::O/minRedefNok/', _FAILED),
        ('P::O/maxNok/', _FAILED),
        ('P::O/maxRedefNok/', _FAILED),
        ('P::O/unitRedefNok/', _FAILED),
        ('P::O/exitConditionNa/', _OK),
        ('P::O/cstOk/', _OK),
        ('P::O/minMaxNok/', _FAILED),
        ('P::O/emptyNa/', _OK),
        ('P::O/definedNa/', _OK),
        ('P::O/diffMinNa/', _OK),
        ('P::O/diffMaxNa/', _OK),
        ('P::Iterated/definedNa/', _OK),
        ('P::Iterated/indexNa/', _OK),
        ('P::Iterated/emptyOk/', _OK),
        ('P::Iterated/minNok/', _FAILED),
        ('P::Iterated/minOk/', _OK),
        ('P::Call/literalNa/', _OK),
        ('P::Call/cstNa/', _OK),
        ('P::Call/definedNa/', _OK),
        ('P::Call/maxOk/', _OK),
    ],
)
def test_identical_for_producer_consumer_nominal(session: suite.Session, path: str, expected: int):
    parameter = '-t SDD_TopLevel'
    rule = IdenticalForProducerConsumer(parameter=parameter)
    model = session.model
    status = rule.on_start(model, parameter=parameter)
    assert status == _OK
    object_ = model.get_object_from_path(path)
    assert object_
    status = rule.on_check_ex(object_, parameter)
    assert status == expected


def test_identical_for_producer_consumer_dobustness(session: suite.Session):
    parameter = '-t SDD_TopLevel'
    rule = IdenticalForProducerConsumer(
        parameter=parameter, min_field='', max_field='', unit_field=''
    )
    model = session.model
    status = rule.on_start(model, parameter=parameter)
    assert status == _OK
    object_ = model.get_object_from_path('P::O/emptyOk/')
    assert object_
    status = rule.on_check_ex(object_, parameter)
    assert status == _OK
