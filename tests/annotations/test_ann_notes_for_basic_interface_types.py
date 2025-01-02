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


from typing import Set

import pytest
import scade.model.suite as suite

from ansys.scade.design_rules.annotations.ann_notes_for_basic_interface_types import (
    AnnNotesForBasicInterfaceTypes,
)
from ansys.scade.design_rules.utils.modelling import get_full_path_ex
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
        'tests/annotations/AnnNotesForBasicInterfaceTypes/' 'AnnNotesForBasicInterfaceTypes.etp'
    )
    return session


@pytest.mark.parametrize(
    'path, expected, items',
    [
        ('P::PublicOk/point/', _OK, {}),
        ('P::PublicOk/lines/', _OK, {}),
        ('P::PublicOk/vectPoints/', _OK, {}),
        ('P::PublicOk/matPoints/', _OK, {}),
        ('P::PublicOk/struct/', _OK, {}),
        ('P::PublicOk/int_/', _OK, {}),
        ('P::PublicOk/bool_/', _OK, {}),
        ('P::PublicOk/char_/', _OK, {}),
        ('P::PublicOk/float_/', _OK, {}),
        ('P::PublicOk/matFloats/', _OK, {}),
        ('P::PublicOk/enum_/', _OK, {}),
        ('P::PublicOk/imported_/', _OK, {}),
        ('P::PublicOk/importedNumeric/', _OK, {}),
        ('P::PublicOk/double/', _OK, {}),
        ('P::PublicOk/speed/', _OK, {}),
        ('P::PublicOk/generic/', _NA, {}),
        ('P::PublicOk/vectGeneric/', _NA, {}),
        ('P::PublicOk/structGeneric/', _NA, {}),
        ('P::PrivateNa/int_/', _NA, {}),
        ('P::PrivateNa/bool_/', _NA, {}),
        ('P::PublicNok/point/', _FAILED, {'P::PointNok/x', 'P::PointNok/y'}),
        ('P::PublicNok/lines/', _FAILED, {'P::PointNok/x', 'P::PointNok/y'}),
        ('P::PublicNok/vectPoints/', _FAILED, {'P::PointNok/x', 'P::PointNok/y'}),
        ('P::PublicNok/matPoints/', _FAILED, {'P::PointNok/x', 'P::PointNok/y'}),
        ('P::PublicNok/matFloats/', _FAILED, {'P::PublicNok/matFloats/'}),
        # TODO: oids not stable for x and c: report the error on anonymous + sub_id=<fieldname>
        (
            'P::PublicNok/anonymous/',
            _FAILED,
            {'P::PublicNok/anonymous/x', 'P::PublicNok/anonymous/c'},
        ),
        (
            'P::PublicNok/struct/',
            _FAILED,
            {
                'P::StructNok/noNote',
                'P::StructNok/default_',
                'P::StructNok/defaultDescription',
                'P::StructNok/noDescription',
                'P::StructNok/noConstraint',
                'P::StructNok/noMin',
                'P::StructNok/noMax',
                'P::StructNok/noUnit',
                # TODO: oids not stable for x: report the error on anonymous + sub_id=<fieldname>
                'P::StructNok/x',
                # TODO: oids not stable for y: report the error on anonymous + sub_id=<fieldname>
                'P::StructNok/y',
                'P::EnumNok/',
                'P::ImportedNok/',
                'P::ImportedNumericNok/',
                'P::PointNok/x',
                'P::PointNok/y',
            },
        ),
        ('P::PublicNok/int_/', _FAILED, {'P::PublicNok/int_/'}),
        ('P::PublicNok/bool_/', _FAILED, {'P::PublicNok/bool_/'}),
        ('P::PublicNok/char_/', _FAILED, {'P::PublicNok/char_/'}),
        ('P::PublicNok/float_/', _FAILED, {'P::PublicNok/float_/'}),
        ('P::PublicNok/enum_/', _FAILED, {'P::EnumNok/'}),
        ('P::PublicNok/imported_/', _FAILED, {'P::ImportedNok/'}),
        ('P::PublicNok/importedNumeric/', _FAILED, {'P::ImportedNumericNok/'}),
        ('P::PublicNok/double/', _FAILED, {'P::DoubleNok/'}),
        ('P::PublicNok/speed/', _FAILED, {'P::DoubleNok/'}),
    ],
)
def test_ann_note_connected_data_for_public_interface_nominal(
    session: suite.Session, path: str, expected: int, items: Set[str]
):
    parameter = '-t SDD_TopLevel --public'
    rule = AnnNotesForBasicInterfaceTypes(parameter=parameter)
    model = session.model
    status = rule.on_start(model, parameter=parameter)
    assert status == _OK
    io = model.get_object_from_path(path)
    assert io
    status = rule.on_check_ex(io, parameter)
    assert status == _NA
    if expected == _OK or expected == _NA:
        assert not rule.violations
    else:
        assert rule.violations
        assert all((_[0] == _FAILED for _ in rule.violations.values()))
        print(len(rule.violations))
        objects = {get_full_path_ex(_[0]) for _ in rule.violations}
        assert objects == items


def test_ann_note_connected_data_for_public_interface_robustness(session: suite.Session):
    parameter = '-t Unknown'
    rule = AnnNotesForBasicInterfaceTypes(parameter=parameter)
    model = session.model
    status = rule.on_start(model, parameter=parameter)
    assert status == _ERROR
