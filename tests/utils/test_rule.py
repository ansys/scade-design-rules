# -*- coding: utf-8 -*-

# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

from ansys.scade.design_rules.utils.rule import Rule, _Rule


def _add_rule_status_23r1(
    self,
    object_: suite.Object,
    status: int,
    message: str,
) -> None:
    # Interface compatible with 2023 R1
    # store the parameters in a list
    self._ut_violations.append((object_, status, message, None))


def _add_rule_status_23r2(
    self,
    object_: suite.Object,
    status: int,
    message: str,
    local_id: str = None,
) -> None:
    # Interface compatible with 2023 R2
    # store the parameters in a list
    self._ut_violations.append((object_, status, message, local_id))


@pytest.mark.parametrize(
    'add_rule_status, expected_local_id',
    [
        (_add_rule_status_23r1, None),
        (_add_rule_status_23r2, '1'),
    ],
)
def test_add_rule_status_version(add_rule_status, expected_local_id):
    # save the original method
    backup = _Rule.add_rule_status
    # set the given method
    _Rule.add_rule_status = add_rule_status
    # perform a call
    rule = Rule(0, '', '', 0)
    rule._ut_violations = []
    rule.add_rule_status(None, Rule.OK, 'test', '1')
    assert rule._ut_violations == [(None, Rule.OK, 'test', expected_local_id)]
    # restore the correct original method
    _Rule.add_rule_status = backup


def test_add_rule_status():
    rule = Rule(0, '', '', 0)
    assert rule.violations == {}
    # add one element
    rule.add_rule_status(None, Rule.OK, 'ok', '1')
    # add different values for the same local_id
    rule.add_rule_status(None, Rule.FAILED, 'failed', '1')
    # add a different local_id
    rule.add_rule_status(None, Rule.ERROR, 'error', '2')
    assert rule.violations == {
        (None, '1'): (Rule.OK, 'ok'),
        (None, '2'): (Rule.ERROR, 'error'),
    }
    rule.on_stop()
    assert rule.violations == {}
