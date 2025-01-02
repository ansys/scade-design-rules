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

"""Implements the NoLiterals rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade.model.suite as suite

import ansys.scade.design_rules.utils.predef as predef
from ansys.scade.design_rules.utils.rule import Rule


class NoLiterals(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0058',
        category='Modelling',
        severity=Rule.REQUIRED,
        parameter='true,false',
        label='No literals',
        description=(
            'Literals shall only be used in constant values.\n'
            "parameter: list of exceptions separated by comma: e.g.: 'true,false'"
        ),
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.ConstValue],
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        if parameter is None:
            return Rule.ERROR
        self.exceptions = [_.strip() for _ in parameter.split(',')]

        return Rule.OK

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """
        Return the evaluation status for the input object.

        This rule does not apply for:
        * constants
        * type of internal variables
        * number of accumulators for iterators
        * patterns of case operator
        * labels of projections
        """
        if object_.kind == 'Label':
            # projection
            return Rule.NA
        elif self._is_case_pattern(object_):
            return Rule.NA
        elif self._is_accumulator_number(object_):
            return Rule.NA

        container = self.get_closest_annotatable(object_)
        if isinstance(container, suite.Constant):
            return Rule.NA
        elif isinstance(container, suite.LocalVariable) and container.is_internal():
            # literals accepted for computed types of internal variables
            return Rule.NA

        violated = object_.value not in self.exceptions
        if violated:
            error_msg = 'Literal found outside constant value (%s)' % object_.value
            identifier = object_.value
            self.add_rule_status(container, Rule.FAILED, error_msg, identifier)

        return Rule.NA

    def _is_case_pattern(self, expression: suite.Expression) -> bool:
        sequence = expression.owner
        if (
            not isinstance(sequence, suite.ExprCall)
            or sequence.predef_opr != predef.SC_ECK_SEQ_EXPR
        ):
            return False
        call = sequence.owner
        if not isinstance(call, suite.ExprCall) or call.predef_opr != predef.SC_ECK_CASE:
            return False
        return sequence == call.parameters[2]

    def _is_accumulator_number(self, expression: suite.Expression) -> bool:
        call = expression.owner
        mapfolds = {
            predef.SC_ECK_MAPFOLD,
            predef.SC_ECK_MAPFOLDI,
            predef.SC_ECK_MAPFOLDW,
            predef.SC_ECK_MAPFOLDWI,
        }
        return (
            isinstance(call, suite.ExprCall)
            and call.predef_opr in mapfolds
            and expression == call.parameters[1]
        )


if __name__ == '__main__':
    # rule instantiated outside of a package
    NoLiterals()
