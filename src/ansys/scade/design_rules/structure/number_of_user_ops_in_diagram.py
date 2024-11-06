# -*- coding: utf-8 -*-

# Copyright (C) 2021 - 2024 ANSYS, Inc. and/or its affiliates.
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

"""Implements the NumberOfUserOpsInDiagram rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class NumberOfUserOpsInDiagram(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0074',
        category='Structuring',
        severity=Rule.REQUIRED,
        parameter='7',
        label='Number of user operators in diagram',
        description=(
            'Number of graphical user-operator instances within a single diagram.\n'
            "Parameter: maximum value: e.g.: '7'"
        ),
    ):
        super().__init__(
            id=id,
            category=category,
            label=label,
            description=description,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            types=[suite.NetDiagram],
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
        violated = False
        user_ops = 0

        for present_element in object_.presentation_elements:
            if isinstance(present_element, suite.EquationGE):
                equation = present_element.equation
                right = equation.right
                if isinstance(right, suite.ExprCall):
                    # only graphical instances
                    if right.operator and present_element.kind == 'FI_EQUATION':
                        user_ops += 1

        if user_ops > int(parameter):
            violated = True

        if violated:
            self.set_message(
                'Too many user operators in diagram (' + str(user_ops) + ' > ' + parameter + ')'
            )
            return Rule.FAILED

        return Rule.OK


if __name__ == '__main__':
    # rule instantiated outside of a package
    NumberOfUserOpsInDiagram()
