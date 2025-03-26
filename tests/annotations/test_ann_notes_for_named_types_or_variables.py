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

from ansys.scade.design_rules.annotations.ann_notes_for_named_types_or_variables import (
    AnnNotesForNamedTypesOrVariables,
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
        'tests/annotations/AnnNotesForNamedTypesOrVariables/AnnNotesForNamedTypesOrVariables.etp'
    )
    return session


@pytest.mark.parametrize(
    'path, expected',
    [
        ('P::Point/', _OK),
        ('P::ImportedOk/', _OK),
        ('P::ImportedNumericOk/', _OK),
        ('P::ImportedNumericNok/', _FAILED),
        ('P::EnumOk/', _OK),
        ('P::EnumNok/', _FAILED),
        ('P::DoubleOk/', _OK),
        ('P::DoubleNok/', _FAILED),
        ('P::SpeedNok/', _FAILED),
        ('P::SpeedOk/', _OK),
        ('P::O/pointOk/', _OK),
        ('P::O/matDoubleNok/', _FAILED),
        ('P::O/matDoubleOk/', _OK),
        ('P::O/matUintOk/', _OK),
        ('P::O/matUintNok/', _FAILED),
        ('P::O/doubleOk/', _OK),
        ('P::O/doubleNok/', _FAILED),
        ('P::O/speedOk/', _OK),
        ('P::O/speedNok/', _FAILED),
        ('P::O/predefOk/', _OK),
        ('P::O/predefNok/', _FAILED),
    ],
)
def test_ann_notes_for_named_types_or_variables_nominal(
    session: suite.Session, path: str, expected: int
):
    parameter = '-t SDD_TopLevel'
    rule = AnnNotesForNamedTypesOrVariables(parameter=parameter)
    model = session.model
    status = rule.on_start(model, parameter=parameter)
    assert status == _OK
    object_ = model.get_object_from_path(path)
    assert object_
    status = rule.on_check_ex(object_, parameter)
    assert status == expected
