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

from ansys.scade.design_rules.annotations.ann_notes_present_and_not_empty import (
    AnnNotesPresentAndNotEmpty,
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
        'tests/annotations/AnnNotesPresentAndNotEmpty/AnnNotesPresentAndNotEmpty.etp'
    )
    return session


@pytest.mark.parametrize(
    'path, parameter, expected',
    [
        ('P::C/', '-t AnnType -n Empty', _FAILED),
        ('P::C/', '-t AnnType -n Default', _FAILED),
        ('P::C/', '-t AnnType -n String Empty', _FAILED),
        ('P::C/', '-t AnnType -n String', _OK),
        ('P::C/', '-t AnnType -n Number;String', _OK),
        ('P::C/', '-t AnnType,notes=String;Number', _OK),
        ('P::C/', '-t AnnType --names Number', _OK),
        ('P::C/', '-t AnnType --names String Unknown', _FAILED),
        ('P::O/', '-t AnnType --names Number', _FAILED),
    ],
)
def test_ann_notes_present_and_not_empty_nominal(
    session: suite.Session, path: str, parameter: str, expected: int
):
    rule = AnnNotesPresentAndNotEmpty(parameter=parameter)
    model = session.model
    status = rule.on_start(model, parameter=parameter)
    assert status == _OK
    object_ = model.get_object_from_path(path)
    assert object_
    status = rule.on_check_ex(object_, parameter)
    assert status == expected


def test_ann_notes_present_and_not_empty_robustness_types(session: suite.Session):
    # execute the rule with an object that is not annotatable, for example a graphical object
    model = session.model
    o = model.get_object_from_path('P::O/')
    assert o
    ge = o.flows[0].presentation_element
    parameter = '-t AnnType -n Empty'
    rule = AnnNotesPresentAndNotEmpty(parameter=parameter)
    status = rule.on_start(model, parameter=parameter)
    assert status == _OK
    status = rule.on_check_ex(ge, parameter)
    assert status == _NA


@pytest.mark.parametrize(
    'parameter',
    [
        ('-t unknown'),
        ('-t AnnType'),
        ('-t AnnType -n'),
    ],
)
def test_ann_notes_present_and_not_empty_robustness_parameter(
    session: suite.Session, parameter: str
):
    model = session.model
    rule = AnnNotesPresentAndNotEmpty(parameter=parameter, types=[suite.Package])
    status = rule.on_start(model, parameter=parameter)
    assert status == _ERROR
