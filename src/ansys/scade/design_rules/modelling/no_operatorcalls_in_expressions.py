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

"""Implements the NoOperatorCallsInExpressions rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class NoOperatorCallsInExpressions(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0060',
        category='Modelling',
        severity=Rule.REQUIRED,
        parameter='18',
        description=(
            'No operator calls within textual expressions.\n'
            'This rule does not apply for Constants and Transition/IfNode conditions.\n'
            'Exceptions on main level can be given as parameters.\n'
            "parameter: operator IDs separated by comma: e.g.: '18'"
        ),
        label='No operator calls in expressions',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.ExprCall],
            kinds=None,
        )

    def on_start(self, model, parameter):
        """Get the rule's parameters."""
        if model is None:
            self.set_message('No model found, rule cannot be checked.')
            return Rule.ERROR
        self.excepted_operators = [_.strip() for _ in parameter.split(',')]

        return Rule.OK

    def on_check(self, object_, parameter):
        """Return the evaluation status for the input object."""
        violated = False

        # This rule does not apply for Constants
        container = self.get_closest_annotatable(object_)
        if not isinstance(container, suite.Constant):
            # is expression part of an Equation
            equation = object_.equation
            if equation is not None:
                # get graphical element
                equation_ge = equation.equation_ge
                # check whether object is a textual expression. OBJ_LIT most probably OBJECT_LITERAL
                if equation_ge.kind == 'OBJ_LIT':
                    if not self._is_expression_valid(object_):
                        violated = True

        if violated:
            error_msg = 'Textual expression not in line with given format: ' + object_.to_string()
            identifier = object_.to_string()
            self.add_rule_status(container, Rule.FAILED, error_msg, identifier)

        return Rule.NA

    def _is_expression_valid(self, expression) -> bool:
        return str(expression.predef_opr) in self.excepted_operators


if __name__ == '__main__':
    # rule instantiated outside of a package
    NoOperatorCallsInExpressions()
