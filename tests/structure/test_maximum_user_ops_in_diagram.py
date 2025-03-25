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

from ansys.scade.design_rules.metrics.number_of_user_ops_in_diagram import (
    NumberOfUserOpsInDiagram,
)
from ansys.scade.design_rules.structure.maximum_user_ops_in_diagram import (
    MaximumUserOpsInDiagram,
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
    """Unique instance of the test model UserOps."""
    pathname = 'tests/structure/UserOps/UserOps.etp'
    return load_session(pathname)


# instantiation alias
class TestMaximumUserOpsInDiagram(MaximumUserOpsInDiagram):
    __test__ = False

    def __init__(self, parameter=None, **kwargs):
        self.parameter = parameter
        super().__init__(id='', parameter=self.parameter, **kwargs)
        metric = NumberOfUserOpsInDiagram()
        self.stub_metrics({metric.id: metric})

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
        ('P::User/', '4', _FAILED),
        ('P::User/', '5', _OK),
        ('P::User/', '6', _OK),
    ],
)
def test_maximum_user_ops_in_diagram_nominal(session: suite.Session, path, param, expected):
    model = session.model

    operator = model.get_object_from_path(path)
    assert operator and len(operator.diagrams) == 1
    rule = TestMaximumUserOpsInDiagram(parameter=param)
    assert rule.on_start(model) == _OK
    status = rule.on_check(operator.diagrams[0])
    assert status == expected


def test_maximum_user_ops_in_diagram_robustness(session: suite.Session):
    model = session.model

    # parameter without value
    rule = TestMaximumUserOpsInDiagram(parameter='-5')
    assert rule.on_start(model) == _ERROR
