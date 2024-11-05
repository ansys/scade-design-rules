# -*- coding: utf-8 -*-

# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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

from ansys.scade.design_rules.annotations.ann_note_connected_data_for_public_interface import (
    AnnNoteConnectedDataForPublicInterface,
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
        'tests/annotations/AnnNoteConnectedDataForPublicInterface/'
        'AnnNoteConnectedDataForPublicInterface.etp'
    )
    return session


@pytest.mark.parametrize(
    'path, expected',
    [
        ('P::Root/inputOk/', _OK),
        ('P::Root/inputMissingNok/', _FAILED),
        ('P::Root/inputIncorrectNok/', _FAILED),
        ('P::Root/outputOk/', _OK),
        ('P::Root/outputMissingNok/', _FAILED),
        ('P::Root/outputIncorrectNok/', _FAILED),
        ('P::Private/inputOk/', _NA),
        ('P::Private/inputMissingNok/', _NA),
        ('P::Private/inputIncorrectNok/', _NA),
        ('P::Invisible::Public/outputOk/', _NA),
        ('P::Invisible::Public/outputMissingNok/', _NA),
        ('P::Invisible::Public/outputIncorrectNok/', _NA),
    ],
)
def test_ann_note_connected_data_for_public_interface_nominal(
    session: suite.Session, path: str, expected: int
):
    parameter = '-i RTB_i -o RTB_o'
    rule = AnnNoteConnectedDataForPublicInterface(parameter=parameter)
    model = session.model
    status = rule.on_start(model, parameter=parameter)
    assert status == _OK
    print(model.name, path)
    annotatable = model.get_object_from_path(path)
    assert annotatable
    status = rule.on_check_ex(annotatable, parameter)
    assert status == expected


@pytest.mark.parametrize(
    'parameter, expected',
    [
        # backward compatibility
        ('inport=i, outport=o', _OK),
        # missing values
        ('-i i', _ERROR),
        ('-o o', _ERROR),
        (None, _ERROR),
    ],
)
def test_ann_note_connected_data_for_public_interface_parameters(
    session: suite.Session, parameter: str, expected: int
):
    rule = AnnNoteConnectedDataForPublicInterface()
    model = session.model
    status = rule.on_start(model, parameter)
    assert status == expected


def test_ann_note_connected_data_for_public_interface_robustness(session: suite.Session):
    rule = AnnNoteConnectedDataForPublicInterface()
    rule.connected_data = 'Unknown'
    model = session.model
    status = rule.on_start(model)
    assert status == _ERROR
