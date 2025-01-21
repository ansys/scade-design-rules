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

from ansys.scade.design_rules.naming.forbidden_keywords import (
    ForbiddenKeywords,
)
from tests.conftest import load_session

# shorter names
_OK = ForbiddenKeywords.OK
_FAILED = ForbiddenKeywords.FAILED
_ERROR = ForbiddenKeywords.ERROR
_NA = ForbiddenKeywords.NA


@pytest.fixture(scope='session')
def session() -> suite.Session:
    # unique model for these tests
    session = load_session('tests/naming/ForbiddenKeywords/ForbiddenKeywords.etp')
    return session


@pytest.mark.parametrize(
    'path, expected',
    [
        ('P::Nok/class/', _FAILED),
        ('P::Nok/this/', _FAILED),
        ('P::Ok/in/', _OK),
        ('P::Ok/out/', _OK),
    ],
)
def test_forbidden_keywords_nominal(session: suite.Session, path: str, expected: int):
    model = session.model

    io = model.get_object_from_path(path)
    assert io is not None
    rule = ForbiddenKeywords()
    parameter = 'keywords.txt'
    assert rule.on_start(model, parameter) == _OK
    status = rule.on_check(io, parameter)
    assert status == expected


def test_forbidden_keywords_robustness(session: suite.Session):
    model = session.model

    object_ = model.get_object_from_path('P::Ok/eq=')
    assert object_ is not None
    rule = ForbiddenKeywords(types=[suite.Equation])
    parameter = 'keywords.txt'
    assert rule.on_start(model, parameter) == _OK
    status = rule.on_check(object_, parameter)
    assert status == _NA


@pytest.mark.parametrize(
    'parameter, expected',
    [
        ('ubnknown.txt', _ERROR),
    ],
)
def test_forbidden_keywords_parameter(session, parameter: str, expected: int):
    model = session.model

    rule = ForbiddenKeywords()
    assert rule.on_start(model, parameter) == expected
