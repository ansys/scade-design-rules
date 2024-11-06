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

from ansys.scade.design_rules.structure.number_of_diagrams_per_element import (
    NumberOfDiagramsPerElement,
)
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def session():
    """Unique instance of the test model NumberOfDiagrams."""
    pathname = 'tests/structure/NumberOfDiagrams/NumberOfDiagrams.etp'
    return load_session(pathname)


# instantiation alias
class TestNumberOfDiagramsPerElement(NumberOfDiagramsPerElement):
    __test__ = False

    def __init__(self, parameter=None, **kwargs):
        self.parameter = parameter
        super().__init__(id='', parameter=self.parameter, **kwargs)

    def on_start(self, model=None, parameter=None):
        parameter = parameter if parameter else self.parameter
        return super().on_start(model=model, parameter=parameter)

    def on_check(self, object, parameter=None):
        parameter = parameter if parameter else self.parameter
        return super().on_check(object, parameter=parameter)


@pytest.mark.parametrize(
    'path, param, expected',
    [
        # default parameters
        ('Ok3::O/', '3', _OK),
        ('Ok3::O/SM1:State1:', '3', _OK),
        ('Ok3::O/SM1:State1:IfBlock1:then:', '3', _OK),
        ('Ok3::O/SM1:State1:IfBlock1:else:', '3', _OK),
        ('Nok3::O/', '3', _FAILED),
        ('Nok3::O/SM1:State1:', '3', _FAILED),
        ('Nok3::O/SM1:State1:IfBlock1:then:', '3', _FAILED),
        ('Nok3::O/SM1:State1:IfBlock1:else:', '3', _FAILED),
    ],
)
def test_number_of_diagrams_per_element_nominal(session: suite.Session, path, param, expected):
    model = session.model

    data_def = model.get_object_from_path(path)
    if isinstance(data_def, suite.IfAction):
        data_def = data_def.action
    assert data_def
    rule = TestNumberOfDiagramsPerElement(parameter=param)
    assert rule.on_start(model) == _OK
    status = rule.on_check(data_def)
    assert status == expected


def test_number_of_diagrams_per_element_robustness(session: suite.Session):
    model = session.model

    # parameter without value
    rule = TestNumberOfDiagramsPerElement(parameter='-5')
    assert rule.on_start(model) == _ERROR
