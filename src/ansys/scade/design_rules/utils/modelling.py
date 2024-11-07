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

"""Provides utilities for developing rules."""

from enum import Enum
from typing import Union

import scade.model.suite as suite

import ansys.scade.apitools.expr as expr
from ansys.scade.apitools.expr import Eck
from ansys.scade.apitools.prop import get_pragma_tool_text


def get_model(object_: suite.Object) -> suite.Model:
    """
    Get the model in which the object resides.

    This function cannot be called for objects that are not
    defined in a model, such as predefined types, for example.

    Parameters
    ----------
    object_ : suite.Object
        Input object.

    Returns
    -------
    suite.Model
    """
    assert object_.defined_in
    return object_.defined_in.model


def get_top_level_package(object_: suite.Object) -> suite.Package:
    """
    Get the top level package of an object.

    Parameters
    ----------
    object_ : suite.Object
        Input object.

    Returns
    -------
    suite.Package
        Top level package or the model if no package is available.
    """
    container = object_.owner
    while container and not isinstance(container, suite.Package):
        object_ = container
        container = container.owner
    if isinstance(object_, suite.Package):
        return object_
    else:
        return container


def get_owner_package(object_: suite.Object) -> suite.Package:
    """
    Get the package of an object.

    Parameters
    ----------
    object_ : suite.Object
        Input object.

    Returns
    -------
    suite.Package
        Package or the model if no package is available.
    """
    container = object_.owner
    while container and not isinstance(container, suite.Package):
        container = container.owner
    return container


def get_root_container_of_expression(expression: suite.Expression) -> suite.Object:
    """
    Get the root container of an expression.

    Parameters
    ----------
    expression : suite.Expression
        Input expression.

    Returns
    -------
    suite.Object
        First container of the expression that is not an expression.
    """
    container = expression.owner
    while isinstance(container, suite.Expression):
        container = container.owner
    return container


def get_root_container_of_type(type_: suite.Type) -> suite.Object:
    """
    Get the root container of a type.

    Parameters
    ----------
    type_ : suite.Type
        Input type.

    Returns
    -------
    suite.Object
    """
    container = type_.owner
    while isinstance(container, suite.Type):
        container = container.owner
    return container


def is_expression_constant(expression: suite.Expression) -> bool:
    """
    Return whether an expression is a constant.

    Parameters
    ----------
    expression : suite.Expression
        Input expression.

    Returns
    -------
    bool
    """
    if isinstance(expression, suite.ConstValue):
        return True
    elif isinstance(expression, suite.ExprId):
        reference = expression.reference
        return isinstance(reference, suite.Constant)
    else:
        return False


class IR(Enum):
    """Identifies the different roles a variable may have in an iterated call."""

    NONE, INDEX, ACC_IN, ACC_OUT, CONTINUE = range(5)


def get_iter_role(variable: suite.LocalVariable, call: suite.ExprCall) -> IR:
    """
    Return the role that an operator variable may have in an iterated call.

    Parameters
    ----------
    variable : suite.LocalVariable
        Input, hidden input or output of the called operator.
    call : suite.ExprCall
        Call expression to the operator.

    Returns
    -------
    IR
        Role of the variable for the call.
    """
    assert variable.operator is not None
    operator = call.operator
    assert operator == variable.operator
    op = expr.accessor(call)
    if not isinstance(op, expr.IteratorOp):
        return IR.NONE

    # parameters depending on the various iterators
    ix_index = -1  # index of the index input
    ix_continue = -1  # index of the condition output

    # number of accumulators
    assert isinstance(op, expr.IteratorOp)
    count = op.accumulator_count
    if count:
        # the number of accumulator for mapfold* constructs must be a literal
        assert isinstance(count, expr.ConstValue)
        n = int(count.value)
    else:
        # unless specified hereafter for fold* constructs
        n = 0

    if op.code == Eck.MAPFOLD:
        pass
    elif op.code == Eck.MAPFOLDI:
        ix_index = 0
    elif op.code == Eck.MAPFOLDW:
        ix_continue = 0
    elif op.code == Eck.MAPFOLDWI:
        ix_index = 0
        ix_continue = 0
    elif op.code == Eck.FOLD:
        n = 1
    elif op.code == Eck.FOLDI:
        n = 1
        ix_index = 0
    elif op.code == Eck.FOLDW:
        n = 1
        ix_continue = 0
    elif op.code == Eck.FOLDWI:
        n = 1
        ix_index = 0
        ix_continue = 0
    elif op.code == Eck.MAP:
        pass
    elif op.code == Eck.MAPI:
        ix_index = 0
    elif op.code == Eck.MAPW:
        ix_continue = 0
    elif op.code == Eck.MAPWI:
        ix_index = 0
        ix_continue = 0

    # index of the first input accumulator
    ix_in_acc = ix_index + 1
    # index of the first output accumulator
    ix_out_acc = ix_continue + 1

    if variable.is_output():
        if ix_continue != -1 and variable == operator.outputs[ix_continue]:
            return IR.CONTINUE
        elif n > 0 and variable in operator.outputs[ix_out_acc : ix_out_acc + n]:
            return IR.ACC_OUT
    else:
        assert variable.is_input() or variable.is_hidden()
        if ix_index != -1 and variable == (operator.inputs + operator.hiddens)[0]:
            return IR.INDEX
        elif n > 0 and variable in (operator.inputs + operator.hiddens)[ix_in_acc : ix_in_acc + n]:
            return IR.ACC_IN

    # default
    return IR.NONE


def get_full_path_ex(object_: suite.Object) -> str:
    """
    Provide a Scade path for objects that don't have one.

    For objects that don't have a path, the function returns their name
    appended to their owner's path. Otherwise, returns their own path.

    Parameters
    ----------
    object_ : suite.Object
        Input object.

    Returns
    -------
    str
        Scade path of the object.
    """
    # a few objects do not have a path
    if isinstance(object_, suite.CompositeElement):
        return '%s%s' % (object_.owner.get_full_path(), object_.name)
    # default
    return object_.get_full_path()


def get_path(scope: suite.Object, element: suite.Object) -> str:
    """
    Return the relative Scade path of a model element with respect to a scope.

    This function provides a workaround for ``Object.get_path()`` which returns
    a wrong path in some circumstances, for example with state machines.

    Parameters
    ----------
    scope : suite.Object
        Context for computing the relative path.
    element : suite.Object
        Input element.

    Returns
    -------
    str
        Relative Scade path of the element or .its absolute path if it not relative to ``scope``.
    """
    scope_path = scope.get_full_path()
    element_path = element.get_full_path()
    return element_path.lstrip(scope_path)


def get_enum_value(enum: suite.Constant) -> int:
    """
    Get the value of the ``C:enum_val`` kcg pragma of an enumeration value.

    Parameters
    ----------
    enum : suite.Constant
        Input enumeration value.

    Returns
    -------
    int
        Value of the kcg pragma ``C:enum_val`` if present, otherwise -1.
    """
    value = get_pragma_tool_text(enum, 'kcg', 'C:enum_val')
    return int(value) if value else -1


def is_numeric(type_: suite.Type) -> bool:
    """
    Return whether a type is numeric.

    Parameters
    ----------
    type_ : Type
        Input type.

    Returns
    -------
    bool
    """
    if isinstance(type_, suite.NamedType):
        if type_.is_predefined():
            return type_.name != 'bool' and type_.name != 'char'
        elif type_.is_generic() or type_.is_imported():
            # all the existing constraints are numeric
            return type_.constraint is not None
        else:
            # unknown
            return False
    else:
        return isinstance(type_, suite.SizedType)


def string_to_integer_float(string: str) -> Union[int, float]:
    """
    Return the numeric value of a Scade literal, by removing its suffix.

    The suffix is _[u]i[8|16|32|64] for integers of _f[32|64]for floats.

    Parameters
    ----------
    string : str
        Input Scade literal.

    Returns
    -------
    int | float
        Value as integer or float, depending on the type of the literal.
    """
    value = string.split('_')[0]
    if '.' in value:
        return float(value)
    else:
        return int(value)


def get_value_from_const(expression: suite.Expression) -> Union[int, float]:
    """
    Calculate the value of a Constant or ConstValue.

    Parameters
    ----------
    expression : suite.Expression
        Input expression.

    Returns
    -------
    int | float
        Value as integer or float, depending on the type of the literal.
    """
    if isinstance(expression, suite.ConstValue):
        val = expression.get_value()
        return string_to_integer_float(val)
    elif isinstance(expression, suite.Constant):
        return get_value_from_const(expression.value)
    else:
        expr_val = expression.evaluate_expression()
        return string_to_integer_float(expr_val)


def is_visible(element: suite.StorageElement) -> bool:
    """
    Return whether a package's declaration is visible.

    Parameters
    ----------
    declaration : StorageElement
        Input declaration.

    Returns
    -------
    bool
        Whether the element is visible, as well as its containing packages.
    """
    return isinstance(element.owner, suite.Model) or (
        element.visibility == 'Public' and is_visible(element.owner)
    )
