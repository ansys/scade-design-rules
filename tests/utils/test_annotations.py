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

from typing import List, Optional, Tuple

import pytest
import scade.model.suite as suite

import ansys.scade.design_rules.utils.annotations as annotations
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session


@pytest.fixture(scope='session')
def session() -> suite.Session:
    # unique model for these tests
    session = load_session('tests/utils/Annotations/Annotations.etp')
    return session


@pytest.mark.parametrize('name, expected', [('Note', True), ('Unknown', False)])
def test_get_note_type(session: suite.Session, name: str, expected: bool):
    model = session.model
    type_ = annotations.get_note_type(model, name)
    exists = type_ is not None
    assert exists == expected


@pytest.mark.parametrize(
    'path, name, expected',
    [
        ('O/', 'Note', ['Note_1']),
        ('O/', 'Unused', []),
        ('O/two/', 'Note', ['Note_1', 'Note_2']),
        ('O/none/', 'Note', []),
    ],
)
def test_get_notes_by_type(session: suite.Session, path: str, name: str, expected: List[str]):
    model = session.model
    type_ = annotations.get_note_type(model, name)
    assert type_
    annotatable = model.get_object_from_path(path)
    assert annotatable
    notes = [_.name for _ in annotations.get_notes_by_type(annotatable, type_)]
    assert notes == expected


@pytest.mark.parametrize(
    'path, name, expected',
    [
        ('O/', 'Note', 'Note_1'),
        ('O/', 'Unused', None),
        ('O/two/', 'Note', 'Note_1'),
        ('O/none/', 'Note', None),
    ],
)
def test_get_first_note_by_type(
    session: suite.Session,
    path: str,
    name: str,
    expected: Optional[str],
):
    model = session.model
    type_ = annotations.get_note_type(model, name)
    assert type_
    annotatable = model.get_object_from_path(path)
    assert annotatable
    note = annotations.get_first_note_by_type(annotatable, type_)
    assert expected == (note.name if note else None)


@pytest.mark.parametrize(
    'path, expected',
    [
        # nominal
        ('O/two/', (True, 'First')),
        # no annotation
        ('O/none/', (False, '')),
        # no value
        ('O/empty/', (False, '')),
        # value is '-'
        ('O/dash/', (False, '-')),
    ],
)
def test_is_ann_note_value_defined_and_get_value(
    session: suite.Session,
    path: str,
    expected: Tuple[bool, str],
):
    # hard-coded values: note -> 'Note', attribute -> 'String'
    model = session.model
    type_ = annotations.get_note_type(model, 'Note')
    assert type_
    annotatable = model.get_object_from_path(path)
    assert annotatable
    note = annotations.get_first_note_by_type(annotatable, type_)
    print('note', note)
    defined, value = annotations.is_ann_note_value_defined_and_get_value(note, 'String')
    assert (defined, value) == expected


@pytest.mark.parametrize(
    'parameter, expected_name, expected_status',
    [
        # backawrd compatibility
        ('notetype=Note', 'Note', Rule.OK),
        # new syntax
        ('-t Note', 'Note', Rule.OK),
        ('--note_type Note', 'Note', Rule.OK),
        # no annotation
        ('', "don't care", Rule.ERROR),
        # wrong value
        ('-t unknown', "don't care", Rule.ERROR),
    ],
)
def test_annotation_rule(
    session: suite.Session, parameter: str, expected_name: str, expected_status: int
):
    rule = annotations.AnnotationRule('', '', '', Rule.REQUIRED)
    status = rule.on_start(session.model, parameter)
    if rule.options:
        if rule.note_type:
            assert status == Rule.OK
            assert rule.note_type.name == expected_name
        else:
            assert status == Rule.ERROR
    else:
        assert status == Rule.ERROR
    assert status == expected_status
