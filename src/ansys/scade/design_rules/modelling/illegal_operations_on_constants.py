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

"""Implements the IllegalOperationsOnConstants rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade.model.suite as suite

from ansys.scade.apitools import print
from ansys.scade.design_rules.utils.naming import substitute_names
from ansys.scade.design_rules.utils.rule import Rule


class IllegalOperationsOnConstants(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0028',
        category='Modelling',
        severity=Rule.REQUIRED,
        parameter='1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 21, 22, 23, 24, '
        '25, 33, 40, 43, 44, 46, 47, 51, 52, 60, 63, 67, 68, 69, 70, 71, 72',
        description=(
            'Operator calls with only constant inputs shall not be used '
            'for the operators in parameter.\n'
            'This rule does not apply for Constants and not for Types'
        ),
        label='Illegal operations on constants',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.Equation, suite.IfNode, suite.Transition],
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        self.check_operators = parameter.split(',')
        try:
            self.check_operators = {int(_) for _ in parameter.split(',') if _.strip()}
            return Rule.OK
        except ValueError:
            pass
        message = "'%s': syntax error" % parameter
        print(message)
        return Rule.ERROR

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        expression = None
        if isinstance(object_, suite.Equation):
            expression = object_.right
        elif isinstance(object_, suite.IfNode):
            expression = object_.expression
        elif isinstance(object_, suite.Transition):
            expression = object_.condition
        else:
            return Rule.OK

        # search for expression calls
        if isinstance(expression, suite.ExprCall):
            # constant sub-expressions
            self.found_elements = []
            # resolution of internal_variables
            self.aliases = {}

            if self._search_through_expr_calls_const(expression):
                # the entire expression is constant
                assert not self.found_elements
                self.found_elements.append(expression.to_string())

            if self.found_elements:
                # replace internal variables by their constants
                elements = [substitute_names(_, self.aliases) for _ in self.found_elements]
                message = 'Illegal operation on Constant found (%s)' % ', '.join(elements)
                self.set_message(message)
                return Rule.FAILED

        return Rule.OK

    def _search_through_expr_calls_const(self, expr_call) -> bool:
        # check only selected operators
        operator = expr_call.predef_opr

        # constant sub-expressions are recorded (side-effect) if the current expression
        # is not constant, otherwise, will be recorded by the caller
        sub_constant_expressions = []
        # if the operator is not part of the checked ones, check the
        # sub-expressions, but do not consider expr_call to be constant
        all_inputs_are_constants = operator in self.check_operators

        operands = expr_call.parameters
        # go through all operands of the expression call
        for operand in operands:
            # resolve only internal variables, only once
            # ==> named constant flows are ignored
            if isinstance(operand, suite.ExprId):
                producer = operand.reference
                if isinstance(producer, suite.LocalVariable) and producer.is_internal():
                    # must be only one and only one definition
                    assert len(producer.definitions) == 1
                    operand = producer.definitions[0].right
                    # replace the internal variable with its producer and store the alias
                    self.aliases[producer.name] = '(' + operand.to_string() + ')'

            if isinstance(operand, suite.ExprId):
                if not isinstance(operand.reference, suite.Constant):
                    all_inputs_are_constants = False
            elif isinstance(operand, suite.ExprCall):
                if self._search_through_expr_calls_const(operand):
                    sub_constant_expressions.append(operand.to_string())
                else:
                    all_inputs_are_constants = False

        if not all_inputs_are_constants:
            # store the found constant expressions
            self.found_elements.extend(sub_constant_expressions)
        return all_inputs_are_constants


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    IllegalOperationsOnConstants()
