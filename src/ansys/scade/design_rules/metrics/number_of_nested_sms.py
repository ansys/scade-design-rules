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

"""Implements the NumberOfNestedSMs metric."""

if __name__ == '__main__':  # pragma: no cover
    # metric instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

import scade.model.suite as suite

from ansys.scade.design_rules.utils.metric import Metric


class NumberOfNestedSMs(Metric):
    """Implements the metric interface."""

    def __init__(
        self,
        id='id_0129',
        category='Counters',
        label='Number of nested state machines',
        description='Number of nested state machines.',
    ):
        super().__init__(
            id=id,
            label=label,
            category=category,
            description=description,
            types=[suite.StateMachine],
            kinds=None,
        )

    def on_compute_ex(self, object_: suite.Object) -> int:
        """Compute the metric for the input object."""
        self.nested_sms = 0
        self._check_sm(object_, 1)
        self.set_result_metric(self.nested_sms)

        return Metric.OK

    def _check_sm(self, state_machine: suite.StateMachine, level: int):
        if level > self.nested_sms:
            self.nested_sms = level
        for state in state_machine.states:
            self._check_action_or_state(state, level)

    def _check_activate_block(self, activate_block: suite.ActivateBlock, level: int):
        if isinstance(activate_block, suite.IfBlock):
            self._check_if_branch(activate_block.if_node, level)
        else:
            # assert isinstance(activate_block, suite.WhenBlock):
            for when_branch in activate_block.when_branches:
                self._check_action_or_state(when_branch.action, level)

    def _check_if_branch(self, if_branch: suite.IfBranch, level: int):
        if isinstance(if_branch, suite.IfNode):
            self._check_if_branch(if_branch.then, level)
            self._check_if_branch(if_branch._else, level)
        else:
            # assert isinstance(if_branch, suite.IfAction):
            self._check_action_or_state(if_branch.action, level)

    def _check_action_or_state(self, datadef: suite.DataDef, level: int):
        for activate_block in datadef.activate_blocks:
            self._check_activate_block(activate_block, level)
        for state_machine in datadef.state_machines:
            self._check_sm(state_machine, level + 1)


if __name__ == '__main__':  # pragma: no cover
    # metric instantiated outside of a package
    NumberOfNestedSMs()
