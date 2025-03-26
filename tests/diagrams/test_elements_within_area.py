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

from ansys.scade.design_rules.diagrams.elements_within_area import ElementsWithinArea
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def model():
    """Unique instance of the test model Graphics."""
    pathname = 'tests/diagrams/Graphics/Graphics.etp'
    return load_session(pathname).model


@pytest.mark.parametrize(
    'path, expected',
    [
        ('P::Custom/SmOk:', _OK),
        ('P::Custom/SmNok:', _FAILED),
    ],
)
def test_elements_within_area_custom(model: suite.Model, path: str, expected: int):
    element = model.get_object_from_path(path)
    assert element
    rule = ElementsWithinArea()
    status = rule.on_check(element)
    assert status == expected


@pytest.mark.parametrize(
    'path, expected',
    [
        ('P::Custom/SmOk:', _OK),
        ('P::Custom/SmNok:', _FAILED),
        ('P::Nok/SmNok:', _FAILED),
        ('P::Nok/SmNok:StateNok:', _FAILED),
        ('P::Nok/SmNok:StateOk:', _OK),
        ('P::Nok/SmNok:StateOk:<1>:', _FAILED),
        ('P::Nok/SmNok:StateOk:<2>:', _FAILED),
        ('P::Nok/SmNok:StateOk:<3>:', _FAILED),
        ('P::Nok/SmNok:StateOk:<3.1>:', _FAILED),
        ('P::Nok/SmNok:StateOk:<3.2>:', _FAILED),
        ('P::Nok/SmNok:StateOk:<4>:', _FAILED),
        ('P::Nok/IfBlockNok:', _FAILED),
        ('P::Nok/localNok=', _FAILED),
        # terminators can't be found
        # ('P::Nok/_=', _FAILED),
        ('P::Nok/_L3=', _FAILED),
        ('P::Nok/WhenBlockNok:', _FAILED),
        # terminators can't be found
        # ('P::Nok/_=', _FAILED),
        ('P::Nok/Anok/', _FAILED),
        ('P::Ok/SmOk:', _OK),
        ('P::Ok/SmOk:StateNok:', _OK),
        ('P::Ok/SmOk:StateOk:', _OK),
        ('P::Ok/SmOk:StateOk:<1>:', _OK),
        ('P::Ok/SmOk:StateOk:<2>:', _OK),
        ('P::Ok/SmOk:StateOk:<3>:', _OK),
        ('P::Ok/SmOk:StateOk:<3.1>:', _OK),
        ('P::Ok/SmOk:StateOk:<3.2>:', _OK),
        ('P::Ok/SmOk:StateOk:<4>:', _OK),
        ('P::Ok/IfBlockOk:', _OK),
        ('P::Ok/localNok=', _OK),
        # terminators can't be found
        # ('P::Ok/_=', _OK),
        ('P::Ok/_L3=', _OK),
        ('P::Ok/WhenBlockOk:', _OK),
        # terminators can't be found
        # ('P::Ok/_=', _OK),
        ('P::Ok/Aok/', _OK),
    ],
)
def test_elements_within_area_nominal(model: suite.Model, path: str, expected: int):
    element = model.get_object_from_path(path)
    assert element
    rule = ElementsWithinArea()
    status = rule.on_check(element)
    assert status == expected


@pytest.mark.parametrize(
    'path, expected',
    [
        ('P::Na/o=', _NA),
        # project file patched with wrong values
        ('P::Robustness/o=', _FAILED),
    ],
)
def test_elements_within_area_robustness(model: suite.Model, path: str, expected: int):
    element = model.get_object_from_path(path)
    assert element
    rule = ElementsWithinArea()
    status = rule.on_check(element)
    assert status == expected


def test_elements_within_area_cache(model: suite.Model):
    element = model.get_object_from_path('P::Ok/SmOk:')
    assert element
    rule = ElementsWithinArea()
    assert rule.set_boundaries(element.presentation_element.diagram)
    for path, expected in [
        ('P::Ok/SmOk:StateOk:', Rule.OK),
        ('P::Ok/SmOk:', Rule.OK),
        ('P::Robustness/o=', Rule.FAILED),
        ('P::Robustness/_L1=', Rule.NA),
    ]:
        element = model.get_object_from_path(path)
        assert element
        assert rule.on_check(element) == expected


@pytest.mark.parametrize(
    'test_case',
    [
        (None, _OK),
        ('', _OK),
        ('0, 10', _ERROR),
        ('margins=20', _ERROR),
        ('margins = a; b', _ERROR),
        ('margins = 123; 456', _OK),
    ],
)
def test_elements_within_area_parameter(model, test_case):
    parameter, expected = test_case

    rule = ElementsWithinArea()
    assert rule.on_start(model, parameter) == expected


@pytest.mark.parametrize(
    'test_case',
    [
        ('P::Custom/SmOk:', 0, 0, _OK),
        ('P::Custom/SmOk:', 2500, 0, _FAILED),
        ('P::Custom/SmOk:', 0, 5000, _FAILED),
    ],
)
def test_elements_within_area_margins(model, test_case):
    path, x, y, expected = test_case

    rule = ElementsWithinArea()
    parameter = 'margins= %d; %d' % (x, y)
    assert rule.on_start(model, parameter) == _OK
    element = model.get_object_from_path(path)
    assert element
    assert rule.on_check(element) == expected
