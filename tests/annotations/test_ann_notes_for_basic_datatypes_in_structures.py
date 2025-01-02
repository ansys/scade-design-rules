# -*- coding: utf-8 -*-

# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

from ansys.scade.design_rules.annotations.ann_notes_for_basic_datatypes_in_structures import (
    AnnNotesForBasicDataTypesInStructures,
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
        'tests/annotations/AnnNotesForBasicDataTypesInStructures/'
        'AnnNotesForBasicDataTypesInStructures.etp'
    )
    return session


@pytest.mark.parametrize(
    'path, name, expected',
    [
        ('P::StructNok/', 'noNote', _FAILED),
        ('P::StructNok/', 'default_', _FAILED),
        ('P::StructNok/', 'defaultDescription', _FAILED),
        ('P::StructNok/', 'noDescription', _FAILED),
        ('P::StructNok/', 'noConstraint', _FAILED),
        ('P::StructNok/', 'noMin', _FAILED),
        ('P::StructNok/', 'noMax', _FAILED),
        ('P::StructNok/', 'noUnit', _FAILED),
        ('P::StructOk/', 'int_', _OK),
        ('P::StructOk/', 'bool_', _OK),
        ('P::StructOk/', 'char_', _OK),
        ('P::StructOk/', 'float_', _OK),
        ('P::StructOk/', 'double', _OK),
        ('P::StructOk/', 'enum_', _OK),
        ('P::StructOk/', 'imported_', _OK),
        ('P::StructOk/', 'importedNumeric', _OK),
        ('P::StructOk/', 'sized', _OK),
        ('P::StructOk/', 'speed', _OK),
        ('P::StructOk/', 'point', _NA),
        ('P::StructOk/', 'lines', _NA),
        ('P::StructOk/', 'vectPoints', _NA),
        ('P::StructOk/', 'matPoints', _NA),
        ('P::PointOk/', 'x', _OK),
        ('P::PointOk/', 'y', _OK),
        ('P::AnonymousNok/', 'structNok', _FAILED),
        ('P::AnonymousNok/', 'scalarNok', _FAILED),
        ('P::AnonymousNok/', 'vectNok', _FAILED),
    ],
)
def test_ann_note_connected_data_for_public_interface_nominal(
    session: suite.Session, path: str, name: str, expected: int
):
    parameter = '-t SDD_TopLevel'
    rule = AnnNotesForBasicDataTypesInStructures(parameter=parameter)
    model = session.model
    status = rule.on_start(model, parameter=parameter)
    assert status == _OK
    type_ = model.get_object_from_path(path)
    assert type_
    structure = type_.type
    assert structure
    element = next((_ for _ in structure.elements if _.name == name))
    assert element
    status = rule.on_check_ex(element, parameter)
    assert status == expected


@pytest.mark.parametrize(
    'name, sub_name, expected',
    [
        ('structNok', 'p', _NA),
        ('scalarNok', 'x', _NA),
        ('scalarNok', 'c', _NA),
        ('vectNok', 'v', _NA),
    ],
)
def test_ann_note_connected_data_for_public_interface_anonymous(
    session: suite.Session, name: str, sub_name: str, expected: int
):
    parameter = '-t SDD_TopLevel'
    rule = AnnNotesForBasicDataTypesInStructures(parameter=parameter)
    model = session.model
    status = rule.on_start(model, parameter=parameter)
    assert status == _OK
    type_ = model.get_object_from_path('P::AnonymousNok/')
    assert type_
    structure = type_.type
    assert structure
    element = next((_ for _ in structure.elements if _.name == name))
    assert element
    assert isinstance(element.type, suite.Structure)
    sub_element = next((_ for _ in element.type.elements if _.name == sub_name))
    assert sub_element
    status = rule.on_check_ex(sub_element, parameter)
    assert status == expected
