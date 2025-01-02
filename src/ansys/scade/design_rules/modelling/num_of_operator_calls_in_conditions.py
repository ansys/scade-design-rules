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

"""Implements the NumOfOperatorCallsInConditions rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade
import scade.model.suite as suite

from ansys.scade.design_rules.utils.predef import (
    SC_ECK_AND,
    SC_ECK_EQUAL,
    SC_ECK_GEQUAL,
    SC_ECK_GREAT,
    SC_ECK_LEQUAL,
    SC_ECK_LESS,
    SC_ECK_NEQUAL,
    SC_ECK_NOT,
    SC_ECK_OR,
    SC_ECK_PRJ,
    SC_ECK_SHARP,
    SC_ECK_XOR,
)
from ansys.scade.design_rules.utils.rule import Rule


class NumOfOperatorCallsInConditions(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0075',
        category='Modelling',
        severity=Rule.REQUIRED,
        parameter='calls=4,exc=18',
        description=(
            'Number of logical/comparison operator calls within conditions at '
            'Transitions or IfNodes.\n'
            'Number and Exceptions given as parameters: '
            "'calls=number,exc=op1;op2;etc.'"
        ),
        label='Number of operator calls in conditions',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.IfNode, suite.Transition],
            kinds=None,
        )

    def on_start(self, model, parameter):
        """Get the rule's parameters."""
        self.allowed_pred_ops = [
            SC_ECK_PRJ,
            SC_ECK_AND,
            SC_ECK_OR,
            SC_ECK_XOR,
            SC_ECK_NOT,
            SC_ECK_SHARP,
            SC_ECK_LESS,
            SC_ECK_LEQUAL,
            SC_ECK_GREAT,
            SC_ECK_GEQUAL,
            SC_ECK_EQUAL,
            SC_ECK_NEQUAL,
        ]

        d = self.parse_values(parameter)
        if d is None:
            message = "'%s': parameter syntax error" % parameter
        else:
            calls = d.get('calls')
            exc = d.get('exc', '')
            if not calls:
                message = "'%s': missing 'calls' value" % parameter
            else:
                self.number_of_calls = calls
                self.excepted_operators = {_.strip() for _ in exc.split(';')}
                return Rule.OK

        self.set_message(message)
        scade.output(message + '\n')
        return Rule.ERROR

    def on_check(self, object_, parameter):
        """Return the evaluation status for the input object."""
        violated = False
        self.incorrect = False
        self.levels = 0

        # This rule apply for Transitions and IfNodes
        if isinstance(object_, suite.IfNode):
            expression = object_.expression
        else:
            assert isinstance(object_, suite.Transition)
            expression = object_.condition

        self._check_number_of_calls(expression)

        if (self.levels > int(self.number_of_calls)) or self.incorrect:
            violated = True

        if violated:
            if self.incorrect:
                self.set_message(
                    'Non logical or comparison operators used: ' + expression.to_string()
                )
            else:
                self.set_message('Too many operators used: ' + expression.to_string())
            return Rule.FAILED

        return Rule.OK

    def _check_number_of_calls(self, expr: suite.Expression):
        if isinstance(expr, suite.ExprCall):
            if expr.predef_opr not in self.allowed_pred_ops:
                self.incorrect = True
                return
            if self._is_expression_exception(expr):
                num_new_ops = 0
            else:
                num_new_ops = len(expr.parameters) - 1
                # for "not", "-" numNewOps can be 0 although 1 operator is present
                if num_new_ops < 1:
                    num_new_ops = 1
            self.levels += num_new_ops
            for parameter in expr.parameters:
                self._check_number_of_calls(parameter)

    def _is_expression_exception(self, expr_call: suite.ExprCall) -> bool:
        return str(expr_call.predef_opr) in self.excepted_operators


if __name__ == '__main__':
    # rule instantiated outside of a package
    NumOfOperatorCallsInConditions()
