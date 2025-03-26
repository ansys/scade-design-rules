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

from ansys.scade.design_rules.metrics.number_of_nested_sms import NumberOfNestedSMs
from ansys.scade.design_rules.structure.maximum_nested_sms import MaximumNestedSMs
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def session():
    """Unique instance of the test model NestedSms."""
    pathname = 'tests/structure/NestedSms/NestedSms.etp'
    return load_session(pathname)


# instantiation alias
class TestMaximumNestedSMs(MaximumNestedSMs):
    __test__ = False

    def __init__(self, parameter=None, **kwargs):
        self.parameter = parameter
        super().__init__(id='', parameter=self.parameter, **kwargs)
        metric = NumberOfNestedSMs()
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
        ('P::SmEE/SM1:', '2', _FAILED),
        ('P::SmEE/SM1:State1:IB1:else:else:SM2:', '2', _OK),
        ('P::SmEE/SM1:State1:IB1:else:else:SM2:State2:WB1:true:SM3:', '2', _OK),
        ('P::SmEE/SM1:State1:IB1:then:then:SM4:', '2', _OK),
        ('P::SmET/SM1:State1:IB1:else:else:SM4:', '2', _OK),
        ('P::SmET/SM1:', '2', _FAILED),
        ('P::SmET/SM1:State1:IB1:else:then:SM2:', '2', _OK),
        ('P::SmET/SM1:State1:IB1:else:then:SM2:State2:WB1:true:SM3:', '2', _OK),
        ('P::SmTE/SM1:', '2', _FAILED),
        ('P::SmTE/SM1:State1:IB1:then:else:SM2:', '2', _OK),
        ('P::SmTE/SM1:State1:IB1:then:else:SM2:State2:WB1:true:SM3:', '2', _OK),
        ('P::SmTE/SM1:State1:IB1:then:then:SM4:', '2', _OK),
        ('P::SmTT/SM1:', '2', _FAILED),
        ('P::SmTT/SM1:State1:IB1:else:then:SM4:', '2', _OK),
        ('P::SmTT/SM1:State1:IB1:then:then:SM2:', '2', _OK),
        ('P::SmTT/SM1:State1:IB1:then:then:SM2:State2:WB1:true:SM3:', '2', _OK),
        ('P::SmEE/SM1:', '3', _OK),
        ('P::SmET/SM1:', '3', _OK),
        ('P::SmTE/SM1:', '3', _OK),
        ('P::SmTT/SM1:', '3', _OK),
    ],
)
def test_maximum_nested_sms_nominal(session: suite.Session, path, param, expected):
    model = session.model

    sm = model.get_object_from_path(path)
    assert sm
    rule = TestMaximumNestedSMs(parameter=param)
    assert rule.on_start(model) == _OK
    status = rule.on_check(sm)
    assert status == expected


def test_maximum_nested_sms_robustness(session: suite.Session):
    model = session.model

    # parameter without value
    rule = TestMaximumNestedSMs(parameter='-5')
    assert rule.on_start(model) == _ERROR
