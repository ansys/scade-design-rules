# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

from typing import Set

import pytest
import scade.model.suite as suite

from ansys.scade.design_rules.readability.line_crossing import LineCrossing
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
    """Unique instance of the test model LocalNameUniqueness."""
    pathname = 'tests/readability/LineCrossing/LineCrossing.etp'
    return load_session(pathname)


def get_failed_ids(rule: LineCrossing, object_: suite.Object) -> Set[str]:
    # make sure the violations:
    #  1. refer to object_
    #  2. are NOK
    # and return the set of identifiers
    violations = set()
    for (o, id), (status, _) in rule.violations.items():
        assert status == _FAILED
        assert o == object_
        violations.add(id)
    return violations


@pytest.mark.parametrize(
    'path, equation_path, param, expected',
    [
        ('Failure::CrossingEdges/CrossingEdges', 'Failure::CrossingEdges/_L1=', 'lines=yes', _NA),
        (
            'Failure::CrossingActivate/CrossingActivate',
            'Failure::CrossingActivate/_L3=',
            'lines=yes',
            _NA,
        ),
        (
            'Failure::CrossingPredef/CrossingPredef',
            'Failure::CrossingPredef/_L2=',
            'lines=yes',
            _NA,
        ),
        ('Failure::CrossingVar/CrossingVar', 'Failure::CrossingVar/_L1=', 'lines=yes', _NA),
        ('Failure::MultiLines/MultiLines', 'Failure::MultiLines/_L14=', 'lines=yes', _NA),
        (
            'Failure::CrossingNoPoint/CrossingNoPoint',
            'Failure::CrossingNoPoint/_L2=',
            'lines=yes',
            _NA,
        ),
        (
            'Failure::CrossingAction/CrossingAction',
            'Failure::CrossingAction/IfBlock1:else:_L3=',
            'lines=yes',
            _NA,
        ),
        (
            'Failure::CrossingWhen/CrossingWhen',
            'Failure::CrossingWhen/WhenBlock1:true:_L2=',
            'lines=yes',
            _NA,
        ),
        (
            'Sucess::CrossingNoLines/CrossingNoLines',
            'Success::CrossingNoLines/_L1=',
            'lines=no',
            _NA,
        ),
        ('Sucess::Nominal/Nominal', 'Success::Nominal/_L1=', 'lines=no', _NA),
    ],
)
def test_line_crossing_nominal(session: suite.Session, path, equation_path, param, expected):
    model = session.model

    object_ = get_equation_set_or_diagram_from_path(model, path)
    equation = model.get_object_from_path(equation_path)
    rule = LineCrossing()
    assert rule.on_start(object_, parameter=param) == _OK
    status = rule.on_check(object_, parameter=param)
    assert status == expected
    get_failed_ids(rule, equation)
