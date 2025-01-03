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

"""Implements the MaximumOutgoingTransitionsPerState rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

import scade.model.suite as suite
from scade.model.suite.visitors import Visit

from ansys.scade.design_rules.utils.rule import Rule


class _CountOutgoings(Visit):
    def __init__(self):
        self.count = 0

    def visit_transition(self, transition: suite.Transition, *args):
        if transition.target:
            # leaf, nothing to visit anymore
            self.count += 1
        else:
            super().visit_transition(transition, *args)


class MaximumOutgoingTransitionsPerState(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0072',
        category='Structuring',
        severity=Rule.REQUIRED,
        parameter='7',
        label='Maximum outgoing transitions per state',
        description=(
            "Maximum outgoing transitions per state.\nParameter: maximum value: e.g.: '7'"
        ),
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.State],
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        if not parameter.isdigit():
            self.set_message(
                'Parameter for rule is not an integer or lower than zero: ' + parameter
            )
            return Rule.ERROR

        return Rule.OK

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        visitor = _CountOutgoings()
        for transition in object_.outgoings:
            visitor.visit(transition)
        count = visitor.count

        if count > int(parameter):
            self.set_message(
                'Too many outgoing transitions per state (' + str(count) + ' > ' + parameter + ')'
            )
            return Rule.FAILED

        return Rule.OK


if __name__ == '__main__':
    # rule instantiated outside of a package
    MaximumOutgoingTransitionsPerState()
