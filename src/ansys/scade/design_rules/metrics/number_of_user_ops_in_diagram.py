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

"""Implements the NumberOfUserOpsInDiagram metric."""

if __name__ == '__main__':  # pragma: no cover
    # metric instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

import scade.model.suite as suite

from ansys.scade.design_rules.utils.metric import Metric


class NumberOfUserOpsInDiagram(Metric):
    """Implements the metric interface."""

    def __init__(
        self,
        id='id_0132',
        category='Counters',
        label='Number of user-operators in diagram',
        description='Number of graphical user-operator instances within a diagram.',
    ):
        super().__init__(
            id=id,
            category=category,
            description=description,
            label=label,
            types=[suite.NetDiagram],
            kinds=None,
        )

    def on_compute(self, diagram: suite.NetDiagram) -> int:
        """Compute the metric for the input object."""
        user_ops = 0
        for element in diagram.presentation_elements:
            if isinstance(element, suite.EquationGE):
                equation = element.equation
                right = equation.right
                # consider graphical instances of predefined operators or textual equations
                if isinstance(right, suite.ExprCall):
                    if right.operator and element.kind == 'FI_EQUATION':
                        user_ops += 1
        self.set_result_metric(user_ops)
        return Metric.OK


if __name__ == '__main__':  # pragma: no cover
    # metric instantiated outside of a package
    NumberOfUserOpsInDiagram()
