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

"""Implements the NumberOfOutgoingTransitionsPerState metric."""

if __name__ == '__main__':  # pragma: no cover
    # metric instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

import scade.model.suite as suite
from scade.model.suite.visitors import Visit

from ansys.scade.design_rules.utils.metric import Metric


class _CountOutgoings(Visit):
    def __init__(self):
        self.count = 0

    def visit_transition(self, transition: suite.Transition, *args):
        if transition.target:
            # leaf, nothing to visit anymore
            self.count += 1
        else:
            super().visit_transition(transition, *args)


class NumberOfOutgoingTransitionsPerState(Metric):
    """Implements the metric interface."""

    def __init__(
        self,
        id='id_0125',
        category='Counters',
        label='Number of outgoing transitions per state',
        description='Number of outgoing transitions per state.',
    ):
        super().__init__(
            id=id,
            label=label,
            category=category,
            description=description,
            types=[suite.State],
            kinds=None,
        )

    def on_compute(self, state: suite.State) -> int:
        """Compute the metric for the input object."""
        visitor = _CountOutgoings()
        for transition in state.outgoings:
            visitor.visit(transition)
        self.set_result_metric(visitor.count)

        return Metric.OK


if __name__ == '__main__':  # pragma: no cover
    # metric instantiated outside of a package
    NumberOfOutgoingTransitionsPerState()
