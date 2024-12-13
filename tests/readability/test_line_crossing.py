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


def check_expected(
    rule: LineCrossing, objects: Set[tuple[suite.Equation, Set[tuple[suite.Object, suite.Object]]]]
):
    if not objects:
        assert not rule.violations
    else:
        violations = {(o, id_) for o, id_ in rule.violations.keys()}
        statuses = {status for status, _ in rule.violations.values()}

        expected = set()
        for eq, locs in objects:
            local_vars = [loc for loc in locs]
            crossing_message = ''
            if len(local_vars) == 1:
                crossing_message = local_vars[0].get_oid() + ':box'
            elif len(local_vars) > 1:
                crossing_message = local_vars[0].get_oid() + ':' + local_vars[1].get_oid()
            expected.add((eq, crossing_message))
        assert violations == expected
        assert statuses == {_FAILED}


@pytest.mark.parametrize(
    'path, expected, param',
    [
        (
            'Failure::CrossingActivate/CrossingActivate',
            {
                (
                    'Failure::CrossingActivate/_L3=',
                    ('Failure::CrossingActivate/_L3', 'Failure::CrossingActivate/_L1='),
                )
            },
            'lines=yes',
        ),
        (
            'Failure::CrossingPredef/CrossingPredef',
            {
                (
                    'Failure::CrossingPredef/_L2=',
                    ('Failure::CrossingPredef/_L2', 'Failure::CrossingPredef/_L2='),
                )
            },
            'lines=yes',
        ),
        (
            'Failure::CrossingVar/CrossingVar',
            {
                (
                    'Failure::CrossingVar/_L1=',
                    ('Failure::CrossingVar/_L1', 'Failure::CrossingVar/_L3='),
                )
            },
            'lines=yes',
        ),
        (
            'Failure::CrossingAction/CrossingAction',
            {
                (
                    'Failure::CrossingAction/IfBlock1:else:_L3=',
                    ('Failure::CrossingAction/IfBlock1:else:_L3',),
                )
            },
            'lines=yes',
        ),
        (
            'Failure::CrossingWhen/CrossingWhen',
            {
                (
                    'Failure::CrossingWhen/WhenBlock1:true:_L2=',
                    ('Failure::CrossingWhen/WhenBlock1:true:_L2',),
                )
            },
            'lines=yes',
        ),
        (
            'Failure::CrossingTransition/CrossingTransition',
            {
                (
                    'Failure::CrossingTransition/_L1=',
                    ('Failure::CrossingTransition/_L1', 'Failure::CrossingTransition/SM1'),
                )
            },
            'lines=no',
        ),
        (
            'Failure::CrossingState/CrossingState',
            {
                (
                    'Failure::CrossingState/SM1:State1:_L2=',
                    ('Failure::CrossingState/SM1:State1:_L2',),
                )
            },
            'lines=no',
        ),
        ('Success::Nominal/Nominal', set(), 'lines=no'),
    ],
)
def test_line_crossing_nominal(session: suite.Session, path, expected, param):
    model = session.model
    object_ = get_equation_set_or_diagram_from_path(model, path)
    rule = LineCrossing()
    assert rule.on_start(object_, parameter=param) == _OK
    status = rule.on_check(object_, parameter=param)
    assert status == _NA

    equations_and_ids = {
        (
            model.get_object_from_path(equation),
            (model.get_object_from_path(crossing_object) for crossing_object in crossing_objects),
        )
        for equation, crossing_objects in expected
    }

    check_expected(rule, equations_and_ids)


@pytest.mark.parametrize('line_param', [True, False])
@pytest.mark.parametrize(
    'path, expected',
    [
        (
            'LineLineCrossing::CrossingReCross/CrossingReCross',
            {
                (
                    'LineLineCrossing::CrossingReCross/_L2=',
                    (
                        'LineLineCrossing::CrossingReCross/_L2',
                        'LineLineCrossing::CrossingReCross/_L1',
                    ),
                )
            },
        ),
        # Disabled test, Rule does not detect an Edge crossing itself.
        # It is not really considered a failure but rather than an uncovered case because the
        # implementation would be difficult
        # ('LineLineCrossing::CrossingIn/CrossingIn', {('LineLineCrossing::CrossingIn/_L1=',
        # ('LineLineCrossing::CrossingIn/_L1', 'LineLineCrossing::CrossingIn/_L1'))}, 'lines=yes'),
        (
            'LineLineCrossing::CrossingOut/CrossingOut',
            {
                (
                    'LineLineCrossing::CrossingOut/_L14=',
                    ('LineLineCrossing::CrossingOut/_L15', 'LineLineCrossing::CrossingOut/_L14'),
                )
            },
        ),
        (
            'LineLineCrossing::CrossingEdges/CrossingEdges',
            {
                (
                    'LineLineCrossing::CrossingEdges/_L1=',
                    ('LineLineCrossing::CrossingEdges/_L1', 'LineLineCrossing::CrossingEdges/_L2'),
                )
            },
        ),
        (
            'LineLineCrossing::CrossingMultiples/CrossingMultiples',
            {
                (
                    'LineLineCrossing::CrossingMultiples/_L4=',
                    (
                        'LineLineCrossing::CrossingMultiples/_L4',
                        'LineLineCrossing::CrossingMultiples/_L2',
                    ),
                ),
                (
                    'LineLineCrossing::CrossingMultiples/_L4=',
                    (
                        'LineLineCrossing::CrossingMultiples/_L4',
                        'LineLineCrossing::CrossingMultiples/_L3',
                    ),
                ),
                (
                    'LineLineCrossing::CrossingMultiples/_L1=',
                    (
                        'LineLineCrossing::CrossingMultiples/_L1',
                        'LineLineCrossing::CrossingMultiples/_L4',
                    ),
                ),
            },
        ),
    ],
)
def test_line_crossing_line(session: suite.Session, line_param, path, expected):
    model = session.model
    if line_param:
        param = 'lines=yes'
    else:
        param = 'lines=no'
        expected = set()
    object_ = get_equation_set_or_diagram_from_path(model, path)
    rule = LineCrossing()
    assert rule.on_start(object_, parameter=param) == _OK
    status = rule.on_check(object_, parameter=param)
    assert status == _NA

    equations_and_ids = {
        (
            model.get_object_from_path(equation),
            (model.get_object_from_path(crossing_object) for crossing_object in crossing_objects),
        )
        for equation, crossing_objects in expected
    }
    check_expected(rule, equations_and_ids)


@pytest.mark.parametrize(
    'param,expected',
    [('wrong=yes', _ERROR), ('lines=unknown', _OK)],
)
def test_line_crossing_robustness(session: suite.Session, param, expected):
    model = session.model

    rule = LineCrossing()
    assert rule.on_start(model, parameter=param) == expected
