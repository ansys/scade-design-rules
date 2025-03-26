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

"""Implements the NoStructTableComparisons rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import scade.model.suite as suite

from ansys.scade.apitools.expr import Eck
from ansys.scade.apitools.query import get_leaf_type, is_array, is_structure
from ansys.scade.design_rules.utils.rule import Rule


class NoStructTableComparisons(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0062',
        category='Modelling',
        severity=Rule.REQUIRED,
        description='Structures and/or tables should not be compared directly with each other.',
        label='No structure or table comparisons',
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
        comparison_found = False
        self.warning = 0
        self.warning_text = ''
        predef_op = object_.predef_opr

        if Eck(predef_op) in {Eck.LESS, Eck.LEQUAL, Eck.GREAT, Eck.GEQUAL, Eck.EQUAL, Eck.NEQUAL}:
            for operand in object_.parameters:
                comparison_found = self._is_expression_struct_or_array(operand)
                if comparison_found:
                    break

        if comparison_found:
            container = self.get_closest_annotatable(object_)
            error_msg = 'Comparison of structures/arrays found ( ' + object_.to_string() + ' ) '
            identifier = object_.to_string()
            self.add_rule_status(container, Rule.FAILED, error_msg, identifier)
        elif self.warning == 2:
            # 2 warnings means none of the parameters could be assesed
            container = self.get_closest_annotatable(object_)
            error_msg = 'Check incomplete: ' + self.warning_text
            identifier = object_.to_string()
            self.add_rule_status(container, Rule.FAILED, error_msg, identifier)

        return Rule.NA

    def _is_expression_struct_or_array(self, operand: suite.Expression) -> bool:
        if isinstance(operand, suite.ExprId):
            reference = operand.reference
            if reference:
                return self._is_type_struct_or_array(reference.type)
            # else: incomplete model
        elif isinstance(operand, suite.ExprCall):
            operator = operand.operator
            if operator:
                # user defined operator: must have a single output to be used in a comparison
                if operand.modifier:
                    # partial iterators (w - wi) are not considered: more than one output
                    code = Eck(operand.modifier.predef_opr) if operand.modifier else Eck.NONE
                    if code in {Eck.MAP, Eck.MAPI}:
                        # map produces an array
                        return True
                    elif code in {Eck.MAPFOLD, Eck.MAPFOLDI}:
                        # either the iterated operator's output if 1 accumulator, otherwise True
                        count = int(operand.modifier.parameters[1].value)
                        if count == 0:
                            # one may wonder why using mapfold without accumulator
                            return True
                    elif code in {Eck.FOLD, Eck.FOLDI}:
                        # fall through: the output is the operator's output
                        pass
                # default: regular calls or fold[i] iterations
                assert len(operator.outputs) == 1
                return self._is_type_struct_or_array(operator.outputs[0].type)
            else:
                code = Eck(operand.predef_opr)
                if code in {
                    Eck.CHANGE_ITH,
                    Eck.BLD_STRUCT,
                    Eck.SCALAR_TO_VECTOR,
                    Eck.BLD_VECTOR,
                    Eck.MAKE,
                    Eck.REVERSE,
                    Eck.TRANSPOSE,
                    Eck.SLICE,
                    Eck.CONCAT,
                }:
                    # these operators produce an array or a structure
                    return True
                elif code == Eck.PRJ:
                    flow = operand.parameters[0]
                    if not isinstance(flow, suite.ExprId):
                        # the projections not applied to a variable are not considered:
                        # algorithm too complex for an unlikely use case
                        self.warning += 1
                        self.warning_text = 'check for textual projections missing'
                        return False
                    if flow.reference and flow.reference.type:
                        type_ = flow.reference.type
                        for path in operand.parameters[1:]:
                            type_ = get_leaf_type(type_)
                            # protection against incorrect models
                            try:
                                if isinstance(path, suite.ConstValue) and path.kind == 'Label':
                                    name = path.value
                                    type_ = next(_.type for _ in type_.elements if _.name == name)
                                else:
                                    # get the base type of the array
                                    type_ = type_.type
                            except BaseException:
                                # more to address before involving this rule
                                return False
                        return self._is_type_struct_or_array(type_)
                elif code == Eck.PRJ_DYN:
                    # recurse with the default value
                    return self._is_expression_struct_or_array(operand.parameters[-1])
                # else: iterated predefined operators not considered

        # other use cases: scalar type
        return False

    def _is_type_struct_or_array(self, type_: suite.Type) -> bool:
        return is_array(type_) or is_structure(type_)


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    NoStructTableComparisons()
