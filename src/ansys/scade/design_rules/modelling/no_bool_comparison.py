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

"""Implements the NoBoolComparison rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))

import scade.model.suite as suite

from ansys.scade.apitools.query import get_leaf_type, is_predefined
from ansys.scade.design_rules.utils.naming import substitute_names
from ansys.scade.design_rules.utils.rule import Rule


class NoBoolComparison(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0054',
        category='Modelling',
        severity=Rule.MANDATORY,
        description='Boolean values should not be compared to the constants TRUE or FALSE.',
        label='No boolean comparison',
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

    def on_check(self, object_: suite.Object, parameter: str = '') -> int:
        """Return the evaluation status for the input object."""
        # resolution of internal_variables
        self.aliases = {}

        if self._search_through_expr_calls_const_bool(object_):
            # replace internal variables by their constants
            text = substitute_names(object_.to_string(), self.aliases)
            container = self.get_closest_annotatable(object_)
            error_msg = f'Bool comparison found ({text})'
            identifier = object_.to_string()
            self.add_rule_status(container, Rule.FAILED, error_msg, identifier)

        return Rule.NA

    def _search_through_expr_calls_const_bool(self, expr_call: suite.ExprCall) -> bool:
        # check only comparison operators
        if expr_call.predef_opr not in {20, 21, 22, 23, 24, 25}:
            return False

        operands = expr_call.parameters
        # go through all operands of the expression call
        for operand in operands:
            # resolve only internal variables, only once
            # ==> named constant flows are ignored
            if isinstance(operand, suite.ExprId):
                producer = operand.reference
                if isinstance(producer, suite.LocalVariable) and producer.is_internal():
                    # must be only one and only one definition
                    # assert len(producer.definitions) == 1
                    operand = producer.definitions[0].right
                    # replace the internal variable with its producer and store the alias
                    self.aliases[producer.name] = f'({operand.to_string()})'

            if isinstance(operand, suite.ConstValue):
                if operand.kind == 'Bool':
                    # one operand is a boolean constant, no need to continue
                    return True
            elif isinstance(operand, suite.ExprId):
                if isinstance(operand.reference, suite.Constant):
                    if self._is_bool(operand.reference.type):
                        # one operand is a boolean constant, no need to continue
                        return True

        return False

    def _is_bool(self, type_: suite.Type) -> bool:
        leaf_type = get_leaf_type(type_)
        return is_predefined(leaf_type) and leaf_type.name == 'bool'


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    NoBoolComparison()
