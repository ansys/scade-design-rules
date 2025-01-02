# -*- coding: utf-8 -*-

# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

from ansys.scade.design_rules.traceability.llr_nature import LLRNature
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session
from tests.utils.utils import get_equation_set_or_diagram_from_path

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def session():
    """Unique instance of the test model LLRNature."""
    pathname = 'tests/traceability/LLRNature/LLRNature.etp'
    return load_session(pathname)


@pytest.mark.parametrize(
    'test_case',
    [
        ('P::Operator/Graphical/EquationSetOK/', _OK),
        ('P::Operator/Graphical/EquationSetNOK/', _FAILED),
        ('P::Operator/OK/', _OK),
        ('P::Operator/NOK/', _FAILED),
        ('P::Operator/SM1:OK:', _OK),
        ('P::Operator/SM1:OK:<1>:', _FAILED),
        ('P::Operator/SM1:NOK:', _FAILED),
        ('P::Operator/SM1:NOK:<1>:', _OK),
    ],
)
def test_llr_nature_nominal(session: suite.Session, test_case):
    path, expected = test_case
    model = session.model

    llr = model.get_object_from_path(path)
    if not llr:
        llr = get_equation_set_or_diagram_from_path(model, path)

    assert llr is not None
    rule = LLRNature()
    assert rule.on_start(model, '-t DesignElement') == _OK
    status = rule.on_check(llr)
    assert status == expected


@pytest.mark.parametrize(
    'test_case',
    [
        ('-t DesignElement', _OK),
        ('-n DesignElement', _ERROR),
        ('--note_type DesignElement', _OK),
        # https://docs.python.org/3/library/argparse.html#argument-abbreviations-prefix-matching
        # ('--note DesignElement', _ERROR),
        ('--note DesignElement', _OK),
        ('note=DesignElement', _OK),
        ('-t Unknown', _ERROR),
    ],
)
def test_llr_nature_robustness(session: suite.Session, test_case):
    parameter, expected = test_case
    model = session.model

    rule = LLRNature()
    status = rule.on_start(model, parameter)
    assert status == expected
