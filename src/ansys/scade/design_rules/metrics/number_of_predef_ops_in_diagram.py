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

"""Implements the NumberOfPredefOpsInDiagram metric."""

if __name__ == '__main__':  # pragma: no cover
    # metric instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))

import scade.model.suite as suite

from ansys.scade.design_rules.utils.metric import Metric


class NumberOfPredefOpsInDiagram(Metric):
    """Implements the metric interface."""

    def __init__(
        self,
        id='id_0131',
        category='Counters',
        label='Number of predefined operators in diagram',
        description='Number of graphical primitive operator instances within a diagram.',
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
        predef_ops = 0
        for element in diagram.presentation_elements:
            if isinstance(element, suite.EquationGE):
                equation = element.equation
                right = equation.right
                # consider graphical instances of predefined operators or textual equations
                if isinstance(right, suite.ExprCall):
                    if not right.operator or element.kind == 'OBJ_LIT':
                        predef_ops += 1
        self.set_result_metric(predef_ops)
        return Metric.OK


if __name__ == '__main__':  # pragma: no cover
    # metric instantiated outside of a package
    NumberOfPredefOpsInDiagram()
