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

"""Implements the ConstantIfThenElse rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

import scade.model.suite as suite

import ansys.scade.apitools.expr.access as access
from ansys.scade.apitools.query import get_leaf_type, is_predefined
from ansys.scade.design_rules.utils.rule import Rule


class ConstantIfThenElse(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0011',
        category='Modelling',
        severity=Rule.ADVISORY,
        description=(
            "This rule checks if predefined Operators 'if..then..else' have constant "
            'boolean inputs on the left inputs'
        ),
        label='This operator should not be used with constant inputs of boolean type',
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
        call = access.accessor(object_)
        if isinstance(call, access.IfThenElseOp):
            for expr in [call.if_] + call.then + call.else_:
                if self._find_const_bool_expr(expr):
                    violated = True
                    break
            else:
                violated = False
            if violated:
                container = self.get_closest_annotatable(object_)
                error_msg = 'If..Then..Else with at least one constant boolean input.'
                identifier = object_.to_string()
                self.add_rule_status(container, Rule.FAILED, error_msg, identifier)

        return Rule.NA

    def _find_const_bool_expr(self, param: access.Expression) -> bool:
        if isinstance(param, access.ConstValue):
            return param.value in ['true', 'false']
        elif isinstance(param, access.IdExpression):
            const_check = self._find_const_bool_flow(param.path)
            return const_check
        else:
            return False

    def _find_const_bool_flow(self, var: suite.ConstVar) -> bool:
        if isinstance(var, suite.Constant):
            type_ = get_leaf_type(var.type)
            return is_predefined(type_) and type_.name == 'bool'
        elif not var.definitions:
            return False
        else:
            # return true is all the producers are boolean constants:
            for eq in var.definitions:
                if not self._find_const_bool_expr(access.accessor(eq.right)):
                    return False
            return True


if __name__ == '__main__':
    # rule instantiated outside of a package
    ConstantIfThenElse()
