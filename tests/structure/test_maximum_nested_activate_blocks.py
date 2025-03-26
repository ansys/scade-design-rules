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

from ansys.scade.design_rules.metrics.number_of_nested_activate_blocks import (
    NumberOfNestedActivateBlocks,
)
from ansys.scade.design_rules.structure.maximum_nested_activate_blocks import (
    MaximumNestedActivateBlocks,
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
    """Unique instance of the test model NestedAbs."""
    pathname = 'tests/structure/NestedAbs/NestedAbs.etp'
    return load_session(pathname)


# instantiation alias
class TestMaximumNestedActivateBlocks(MaximumNestedActivateBlocks):
    __test__ = False

    def __init__(self, parameter=None, **kwargs):
        self.parameter = parameter
        super().__init__(id='', parameter=self.parameter, **kwargs)
        metric = NumberOfNestedActivateBlocks()
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
        ('P::IwiET/IB1:', '2', _FAILED),
        ('P::IwiET/IB1:else:then:SM1:State1:WB1:', '2', _OK),
        ('P::IwiET/IB1:else:then:SM1:State1:WB1:true:IB2:', '2', _OK),
        ('P::IwiET/IB1:then:then:WB2:', '2', _OK),
        ('P::IwiTE/IB1:', '2', _FAILED),
        ('P::IwiTE/IB1:else:else:WB2:', '2', _OK),
        ('P::IwiTE/IB1:then:else:SM1:State1:WB1:', '2', _OK),
        ('P::IwiTE/IB1:then:else:SM1:State1:WB1:true:IB2:', '2', _OK),
        ('P::WiwTT/WB1:', '2', _FAILED),
        ('P::WiwTT/WB1:true:IB1:', '2', _OK),
        ('P::WiwTT/WB1:true:IB1:else:else:WB2:', '2', _OK),
        ('P::WiwTT/WB1:true:IB1:else:then:SM1:State1:WB3:', '2', _OK),
        ('P::WiwEE/WB1:', '2', _FAILED),
        ('P::WiwEE/WB1:true:IB1:', '2', _OK),
        ('P::WiwEE/WB1:true:IB1:else:then:SM1:State1:WB3:', '2', _OK),
        ('P::WiwEE/WB1:true:IB1:then:then:WB2:', '2', _OK),
        ('P::IwiET/IB1:', '3', _OK),
        ('P::IwiTE/IB1:', '3', _OK),
        ('P::WiwTT/WB1:', '3', _OK),
        ('P::WiwEE/WB1:', '3', _OK),
    ],
)
def test_maximum_nested_activate_blocks_nominal(session: suite.Session, path, param, expected):
    model = session.model

    sm = model.get_object_from_path(path)
    assert sm
    rule = TestMaximumNestedActivateBlocks(parameter=param)
    assert rule.on_start(model) == _OK
    status = rule.on_check(sm)
    assert status == expected


def test_maximum_nested_activate_blocks_robustness(session: suite.Session):
    model = session.model

    # parameter without value
    rule = TestMaximumNestedActivateBlocks(parameter='-5')
    assert rule.on_start(model) == _ERROR
