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

from ansys.scade.design_rules.metrics.number_of_nested_sms import (
    NumberOfNestedSMs,
)
from ansys.scade.design_rules.utils.rule import Metric
from tests.conftest import load_session

# shorter names
_OK = Metric.OK
_ERROR = Metric.ERROR
_NA = Metric.NA


@pytest.fixture(scope='session')
def session():
    """Unique instance of the NumberOfNestedSMs test model."""
    model = 'NumberOfNestedSMs'
    pathname = f'tests/metrics/{model}/{model}.etp'
    return load_session(pathname)


@pytest.mark.parametrize(
    'path, expected',
    [
        ('P::SmEE/SM1:', 3),
        ('P::SmEE/SM1:State1:IB1:else:else:SM2:', 2),
        ('P::SmEE/SM1:State1:IB1:else:else:SM2:State2:WB1:true:SM3:', 1),
        ('P::SmEE/SM1:State1:IB1:then:then:SM4:', 1),
        ('P::SmET/SM1:', 3),
        ('P::SmET/SM1:State1:IB1:else:else:SM4:', 1),
        ('P::SmET/SM1:State1:IB1:else:then:SM2:', 2),
        ('P::SmET/SM1:State1:IB1:else:then:SM2:State2:WB1:true:SM3:', 1),
        ('P::SmTE/SM1:', 3),
        ('P::SmTE/SM1:State1:IB1:then:else:SM2:', 2),
        ('P::SmTE/SM1:State1:IB1:then:else:SM2:State2:WB1:true:SM3:', 1),
        ('P::SmTE/SM1:State1:IB1:then:then:SM4:', 1),
        ('P::SmTT/SM1:', 3),
        ('P::SmTT/SM1:State1:IB1:else:then:SM4:', 1),
        ('P::SmTT/SM1:State1:IB1:then:then:SM2:', 2),
        ('P::SmTT/SM1:State1:IB1:then:then:SM2:State2:WB1:true:SM3:', 1),
    ],
)
def test_number_of_nested_activate_blocks_nominal(session: suite.Session, path, expected):
    model = session.model

    block = model.get_object_from_path(path)
    assert block
    metric = NumberOfNestedSMs()
    status = metric.on_compute(block)
    assert status == _OK
    result = metric.result
    assert result == expected
