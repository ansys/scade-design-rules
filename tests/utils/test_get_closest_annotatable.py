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

from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session


@pytest.fixture(scope='session')
def session() -> suite.Session:
    # unique model for these tests
    session = load_session('tests/utils/GetClosestAnnotatable/GetClosestAnnotatable.etp')
    return session


def format_test_data(data: list) -> tuple:
    """Add an id to each data, assuming the first element is a Scade path."""
    return [pytest.param(*_, id=_[0].strip('/:=').split('/')[-1]) for _ in data]


@pytest.mark.parametrize(
    'path, subpath',
    format_test_data(
        [
            ('P::O/anonymous/', '.type'),
            ('P::O/', '.typevars[0]'),
            ('P::O/edge=', '.presentation_element'),
            ('P::O/edge=', '.presentation_element.out_edges[0]'),
        ]
    ),
)
def test_get_closest_annotatable(session: suite.Session, path, subpath):
    model = session.model

    object_ = model.get_object_from_path(path)
    assert object_
    element = eval('object_%s' % subpath)
    assert element
    rule = Rule(0, '', '', 0)
    annotatable = rule.get_closest_annotatable(element)
    assert annotatable == object_
