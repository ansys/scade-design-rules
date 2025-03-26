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
from ansys.scade.design_rules.utils.rule import Metric
from tests.conftest import load_session

# shorter names
_OK = Metric.OK
_ERROR = Metric.ERROR
_NA = Metric.NA


@pytest.fixture(scope='session')
def session():
    """Unique instance of the NumberOfNestedActivateBlocks test model."""
    model = 'NumberOfNestedActivateBlocks'
    pathname = f'tests/metrics/{model}/{model}.etp'
    return load_session(pathname)


@pytest.mark.parametrize(
    'path, expected',
    [
        ('P::IwiET/IB1:', 3),
        ('P::IwiET/IB1:else:then:SM1:State1:WB1:', 2),
        ('P::IwiET/IB1:else:then:SM1:State1:WB1:true:IB2:', 1),
        ('P::IwiET/IB1:then:then:WB2:', 1),
        ('P::IwiTE/IB1:', 3),
        ('P::IwiTE/IB1:else:else:WB2:', 1),
        ('P::IwiTE/IB1:then:else:SM1:State1:WB1:', 2),
        ('P::IwiTE/IB1:then:else:SM1:State1:WB1:true:IB2:', 1),
        ('P::WiwEE/WB1:', 3),
        ('P::WiwEE/WB1:true:IB1:', 2),
        ('P::WiwEE/WB1:true:IB1:else:then:SM1:State1:WB3:', 1),
        ('P::WiwEE/WB1:true:IB1:then:then:WB2:', 1),
        ('P::WiwTT/WB1:', 3),
        ('P::WiwTT/WB1:true:IB1:', 2),
        ('P::WiwTT/WB1:true:IB1:else:else:WB2:', 1),
        ('P::WiwTT/WB1:true:IB1:else:then:SM1:State1:WB3:', 1),
    ],
)
def test_number_of_nested_activate_blocks_nominal(session: suite.Session, path, expected):
    model = session.model

    block = model.get_object_from_path(path)
    assert block
    metric = NumberOfNestedActivateBlocks()
    status = metric.on_compute(block)
    assert status == _OK
    result = metric.result
    assert result == expected
