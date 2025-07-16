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

"""Implements the ForbiddenRealComparisons rule."""

from typing import Dict, Optional, Set, Tuple

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.predef import (
    SC_ECK_BLD_STRUCT,
    SC_ECK_CASE,
    SC_ECK_DIV,
    SC_ECK_EQUAL,
    SC_ECK_FBY,
    SC_ECK_FOLLOW,
    SC_ECK_GEQUAL,
    SC_ECK_GREAT,
    SC_ECK_IF,
    SC_ECK_INT2REAL,
    SC_ECK_LEQUAL,
    SC_ECK_LESS,
    SC_ECK_MAKE,
    SC_ECK_NEQUAL,
    SC_ECK_NUMERIC_CAST,
    SC_ECK_PRE,
    SC_ECK_PRJ,
    SC_ECK_PRJ_DYN,
    SC_ECK_REAL2INT,
    SC_ECK_SEQ_EXPR,
    SC_ECK_TIMES,
)
from ansys.scade.design_rules.utils.rule import Rule


class Mask:
    """
    Base class for abstracting a type.

    A mask is considered as float if one of its components is float.
    """

    def __init__(self, is_float=None):
        # cache
        self._is_float = is_float

    def is_float(self) -> bool:
        """Return whether the type is float."""
        return self._is_float is True


class Scalar(Mask):
    """Mask class for scalar types or arrays."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Struct(Mask):
    """Mask class for structure types."""

    def __init__(self, fields=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = fields if fields else {}

    def is_float(self) -> bool:
        """Return whether the type is float."""
        if self._is_float is None:
            # lazy evaluation
            self._is_float = False
            for _, mask in self.fields.items():
                self._is_float |= mask is not None and mask.is_float()
        return self._is_float


class ForbiddenRealComparisons(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0024',
        description='Comparisons of real values are not allowed: = (20, 21, 22, 23, 24, 25)',
        label='Forbidden real comparisons',
        category='Modelling',
        severity=Rule.REQUIRED,
        parameter='20, 21, 22, 23, 24, 25',
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
        # comparison operators specified in the rule's parameters
        self.comp_operators = set()
        # predefined float types
        self.floats: Set[suite.Type] = set()
        # cache for type abstractions
        self.masks: Dict[Optional[suite.Type], Optional[Mask]] = {}

    def on_start(self, model: suite.Model, parameter: str = '') -> int:
        """Cache the predefined types and get the parameters."""
        if not parameter:
            self.set_message('No parameter given, rule cannot be checked.')
            return Rule.ERROR

        self.comp_operators = {int(_) for _ in parameter.split(',') if _} if parameter else set()
        # float types for Scade 6.4 or 6.6
        self.floats = set()
        for name in ('float', 'float32', 'float64'):
            type_ = model.session.find_predefined_type(name)
            if type_:
                self.floats.add(type_)
        # reset cache
        self.masks = {}

        return Rule.OK

    def on_check(self, object_: suite.Object, parameter: str = '') -> int:
        """Return the evaluation status for the input object."""
        assert isinstance(object_, suite.ExprCall)  # nosec B101  # addresses linter
        if object_.predef_opr in self.comp_operators:
            real_found, error = self.handle_expressions(object_.parameters)

            if error:
                # ERROR leads to a fatal error, not correctly reported
                # self.set_message("Error evaluating " + object.to_string() + ", ")
                # return Rule.ERROR
                Rule.OK
            elif real_found:
                self.set_message(f'Real comparison in {object_.to_string()}, ')
                return Rule.FAILED

        return Rule.OK

    def handle_expressions(self, expressions) -> Tuple[bool, bool]:
        """Recurse on expressions elements."""
        result = False
        error = False
        for expr in expressions:
            mask = self.get_expression_mask(expr)
            if mask is None:
                error = True
            else:
                result |= not error and mask.is_float()
        return result, error

    def get_expression_mask(self, expr: suite.Expression) -> Optional[Mask]:
        """Return the type mask for expr."""
        default = Scalar(is_float=False)
        if isinstance(expr, suite.ConstValue):
            # if not float, the returned type does not matter
            return Scalar(is_float=expr.kind == 'Float')
        elif isinstance(expr, suite.ExprId):
            # expr.reference might be None with incomplete models
            return self.get_type_mask(expr.reference.type) if expr.reference else None
        elif isinstance(expr, suite.ExprType):
            # ExprType can't be an operand of a comparison
            # must not be called
            pass  # pragma: no cover
        elif isinstance(expr, suite.ExprText):
            # syntax error
            # must not be called
            pass  # pragma: no cover

        assert isinstance(expr, suite.ExprCall)  # nosec B101  # addresses linter
        if expr.operator:
            # must be a function, check the type ouf the first output
            outputs = expr.operator.outputs
            # assert len(outputs) == 1
            return self.get_type_mask(outputs[0].type) if outputs else default

        # predefined operator: consider the parameters
        # for most of the operators, it is enough to consider the first parameter
        code = expr.predef_opr
        parameters = expr.parameters
        if code in {
            SC_ECK_LESS,
            SC_ECK_LEQUAL,
            SC_ECK_GREAT,
            SC_ECK_GEQUAL,
            SC_ECK_EQUAL,
            SC_ECK_NEQUAL,
            SC_ECK_TIMES,
        }:
            # boolean operator
            return default
        elif code in {SC_ECK_DIV, SC_ECK_REAL2INT}:
            # ensure compatibility with Scade 6.4
            return default
        elif code in {SC_ECK_INT2REAL}:
            # ensure compatibility with Scade 6.4
            return Scalar(is_float=True)
        elif code in {SC_ECK_FOLLOW}:
            # type of the first parameter of the first sequence
            return self.get_expression_mask(expr.parameters[0].parameters[0])
        elif code in {SC_ECK_PRE, SC_ECK_FBY}:
            # type of the first parameter
            return self.get_expression_mask(expr.parameters[0])
        elif code in {SC_ECK_IF, SC_ECK_CASE}:
            # type of the first 'then' or 'case' parameter
            return self.get_expression_mask(expr.parameters[1].parameters[0])
        elif code == SC_ECK_SEQ_EXPR:
            # must not happen
            raise AssertionError('internal error: SEQ_EXPR')  # pragma: no cover
        elif code in {SC_ECK_NUMERIC_CAST, SC_ECK_MAKE}:
            assert isinstance(expr.parameters[1], suite.ExprType)  # nosec B101  # addresses linter
            return self.get_type_mask(expr.parameters[1].reference)
        elif code == SC_ECK_BLD_STRUCT:
            fields = {_.label.name: self.get_expression_mask(_) for _ in parameters}
            return Struct(fields)
        elif code == SC_ECK_PRJ:
            mask = self.get_expression_mask(parameters[0])
            for filter in parameters[1:]:
                if isinstance(filter, suite.ConstValue) and filter.kind == 'Label':
                    if not isinstance(mask, Struct):
                        # semantic error
                        return None
                    mask = mask.fields.get(filter.value)
                # else: ignore indexes
            return mask
        elif code == SC_ECK_PRJ_DYN:
            # consider the default value
            return self.get_expression_mask(parameters[-1])
        else:
            return self.get_expression_mask(parameters[0])

    def get_type_mask(self, type_: suite.Type) -> Optional[Mask]:
        """Return the mask of a type."""
        while isinstance(type_, suite.NamedType):
            if type_.is_predefined() or type_.is_generic():
                break
            type_ = type_.type
        mask = self.masks.get(type_)
        if not mask:
            if isinstance(type_, suite.NamedType):
                if type_.constraint:
                    # polymorphic type
                    is_float = type_.constraint.is_float()
                elif type_.is_predefined():
                    is_float = type_ in self.floats
                else:
                    # incomplete model, alias without definition
                    # or unconstrained polymorphic type
                    is_float = False
                mask = Scalar(is_float)
            elif isinstance(type_, suite.Table):
                return self.get_type_mask(type_.type)
            elif isinstance(type_, suite.Structure):
                fields = {_.name: self.get_type_mask(_.type) for _ in type_.elements}
                mask = Struct(fields)
            elif type_:
                # enumerations, sized types
                mask = Scalar(is_float=False)
            self.masks[type_] = mask
        return mask


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    ForbiddenRealComparisons()
