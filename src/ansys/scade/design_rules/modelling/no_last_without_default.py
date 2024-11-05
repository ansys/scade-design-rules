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

"""Implements the NoLastWithoutDefault rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class NoLastWithoutDefault(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0057',
        category='Modelling',
        severity=Rule.REQUIRED,
        description=(
            "An assignment just as (last 'variable -> (L)variable) shall not be used.\n"
            'Only if a default value is assigned such an statement is necessary.\n'
            'Implicit behaviour of SCADE'
        ),
        label='No last without default',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=False,
            default_param='',
            description=description,
            label=label,
            types=[suite.Equation],
            kinds=None,
        )

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        violated = False
        left_name = ''

        right = object_.right
        if isinstance(right, suite.ExprId) and right.last:
            variable = right.reference
            # if default value is defined do not check further
            if variable.default:
                return Rule.OK

            # find left (shall only be 1) in rights of other equations.
            assert len(object_.lefts) == 1
            left = object_.lefts[0]
            for expr_id in left.expr_ids:
                next_equation = expr_id.owner
                if next_equation:
                    assert len(next_equation.lefts) == 1
                    next_left = next_equation.lefts[0]
                    if next_left == right.reference:
                        left_name = next_left.name
                        violated = True
                        break

        if violated:
            self.set_message(
                "Assignment (last 'variable -> (L)variable) found ( "
                + right.to_string()
                + ' -> '
                + left_name
                + ' )'
            )
            return Rule.FAILED

        return Rule.OK


if __name__ == '__main__':
    # rule instantiated outside of a package
    NoLastWithoutDefault()
