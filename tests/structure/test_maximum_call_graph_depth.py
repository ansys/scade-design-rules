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

from ansys.scade.design_rules.structure.maximum_call_graph_depth import (
    MaximumCallGraphDepth,
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
    """Unique instance of the test model MaximumCallGraphDepth."""
    pathname = 'tests/structure/MaximumCallGraphDepth/MaximumCallGraphDepth.etp'
    return load_session(pathname)


class TestMaximumCallGraphDepth(MaximumCallGraphDepth):
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
        ('Success::NominalPass/', 'depth=8,visibility=Public', _OK),
        ('Failure::NominalFailed/', 'depth=8,visibility=Public', _FAILED),
        ('Success::NominalPrivate/', 'depth=8,visibility=Public', _NA),
        ('Failure::BooleanActivate/', 'depth=8,visibility=Public', _FAILED),
        ('Failure::IfBlock/', 'depth=8,visibility=Public', _FAILED),
        ('Failure::MultipleFailures/', 'depth=8,visibility=Public', _FAILED),
        ('Failure::Restart/', 'depth=8,visibility=Public', _FAILED),
        ('Failure::StateMachine/', 'depth=8,visibility=Public', _FAILED),
        ('Failure::TextualDiagram/', 'depth=8,visibility=Public', _FAILED),
        ('Failure::TextualExpression/', 'depth=8,visibility=Public', _FAILED),
    ],
)
def test_max_call_graph_depth_nominal(session: suite.Session, path, param, expected):
    model = session.model
    op = model.get_object_from_path(path)
    rule = TestMaximumCallGraphDepth(parameter=param)
    assert rule.on_start(op) == _OK
    status = rule.on_check(op)
    assert status == expected

