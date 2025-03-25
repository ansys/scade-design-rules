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

from ansys.scade.design_rules.modelling.forbidden_real_comparisons import ForbiddenRealComparisons
from ansys.scade.design_rules.utils.rule import Rule
from conftest import load_session

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def model():
    """Unique instance of the test model ForbiddenRealComparisons."""
    pathname = 'tests/modelling/ForbiddenRealComparisons/ForbiddenRealComparisons.etp'
    return load_session(pathname).model


# instantiation alias
class TestForbiddenRealComparisons(ForbiddenRealComparisons):
    __test__ = False

    def __init__(self, parameter='20, 21, 22, 23, 24, 25'):
        self.parameter = parameter
        super().__init__(parameter=self.parameter)

    def on_start(self, model=None, parameter=None):
        parameter = parameter if parameter else self.parameter
        return super().on_start(model=model, parameter=parameter)

    def on_check(self, object, parameter=None):
        parameter = parameter if parameter else self.parameter
        return super().on_check(object, parameter=parameter)


@pytest.mark.parametrize(
    'test_case',
    [
        ('P::Op/_L1=', _OK),
        ('P::Op/_L2=', _FAILED),
        # ERROR leads to a fatal error, not correctly reported
        # ('P::Op/_L3=', _ERROR),
        # ('P::Op/_L5=', _ERROR),
        ('P::Op/_L3=', _OK),
        ('P::Op/_L5=', _OK),
    ],
)
def test_forbidden_real_comparisons(model: suite.Model, test_case):
    path, expected_status = test_case

    equation = model.get_object_from_path(path)
    assert equation
    rule = TestForbiddenRealComparisons()
    assert rule.on_start(model) == _OK
    status = rule.on_check(equation.right)
    assert status == expected_status


@pytest.mark.parametrize(
    'test_case',
    [
        # content produced with list_test_float_equations.py from the test project
        # {{
        ('P::IsFloat/_L5=', True),
        ('P::IsFloat/_L6=', True),
        ('P::IsFloat/_L8=', True),
        ('P::IsFloat/_L14=', True),
        ('P::IsFloat/_L15=', True),
        ('P::IsFloat/_L60=', True),
        ('P::IsFloat/_L61=', True),
        ('P::IsFloat/_L63=', True),
        ('P::IsFloat/_L64=', True),
        ('P::IsFloat/_L65=', True),
        ('P::IsFloat/_L66=', True),
        ('P::IsFloat/_L68=', True),
        ('P::IsFloat/_L69=', True),
        ('P::IsFloat/_L70=', True),
        ('P::IsFloat/_L71=', True),
        ('P::IsFloat/_L72=', True),
        ('P::IsFloat/_L73=', True),
        ('P::IsFloat/_L74=', True),
        ('P::IsFloat/_L75=', True),
        ('P::IsFloat/_L19=', False),
        ('P::IsFloat/_L20=', False),
        ('P::IsFloat/_L21=', False),
        ('P::IsFloat/_L25=', False),
        ('P::IsFloat/_L28=', False),
        ('P::IsFloat/_L33=', False),
        ('P::IsFloat/_L34=', False),
        ('P::IsFloat/_L39=', False),
        ('P::IsFloat/_L40=', False),
        ('P::IsFloat/_L43=', False),
        ('P::IsFloat/_L45=', False),
        ('P::IsFloat/_L47=', False),
        ('P::IsFloat/_L49=', False),
        ('P::IsFloat/_L51=', False),
        ('P::IsFloat/_L52=', False),
        ('P::IsFloat/_L56=', False),
        ('P::IsFloat/_L57=', False),
        ('P::IsFloat/_L58=', False),
        # }}
    ],
)
def test_get_expression_mask(model: suite.Model, test_case):
    path, expected_is_float = test_case

    equation = model.get_object_from_path(path)
    assert equation
    rule = TestForbiddenRealComparisons()
    assert rule.on_start(model) == _OK
    mask = rule.get_expression_mask(equation.right)
    is_float = mask.is_float() if mask else None
    assert is_float == expected_is_float
