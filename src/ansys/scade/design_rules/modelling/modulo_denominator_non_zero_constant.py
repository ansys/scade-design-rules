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

"""Implements the ModuloDenominatorNonZeroConstant rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.modelling import get_value_from_const
from ansys.scade.design_rules.utils.rule import Rule


class ModuloDenominatorNonZeroConstant(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0119',
        category='Modelling',
        severity=Rule.REQUIRED,
        label='Modulo operations shall use a non zero constant as denominator.',
        description='Modulo operations shall use a non zero constant as denominator.',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=False,
            default_param='',
            description=description,
            label=label,
            types=[suite.ExprCall],
            kinds=None,
        )

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        violated = False
        message = ''

        expr_call = object_
        if expr_call.predef_opr_id == 'SC_ECK_MOD':
            denominator_expr = expr_call.parameters[1]
            if isinstance(denominator_expr, suite.ExprId):
                reference = denominator_expr.reference
                if isinstance(reference, suite.LocalVariable):
                    equations = reference.definitions
                    for equation in equations:
                        right = equation.right
                        if isinstance(right, suite.ExprId):
                            denominator = right.reference
                        elif isinstance(right, suite.ConstValue):
                            denominator = right
                elif isinstance(reference, suite.Constant):
                    denominator = reference
                else:
                    pass
            elif isinstance(denominator_expr, suite.ConstValue):
                denominator = denominator_expr
            else:
                pass

            try:
                const_value = get_value_from_const(denominator)
                if const_value == 0:
                    message = 'Modulo has non zero denominator.'
                    violated = True
            except Exception:
                violated = True
                message = 'Denominator cannot be evaluated.'

        if violated:
            container = self.get_closest_annotatable(object_)
            identifier = object_.to_string()
            self.add_rule_status(container, Rule.FAILED, message, identifier)

        return Rule.NA


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    ModuloDenominatorNonZeroConstant()
