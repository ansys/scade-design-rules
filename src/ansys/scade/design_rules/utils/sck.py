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

"""Provides an enumeration for finer grain discrimination, mostly used for naming rules."""

from enum import Enum

import scade.model.suite as suite


class SCK(Enum):
    """
    Finer grain discrimination, mostly used for naming rules.

    --> address only named objects
    """

    MODEL = (suite.Model, lambda o: True)
    PACKAGE = (suite.Package, lambda o: not isinstance(o, suite.Model))
    TYPE = (suite.NamedType, lambda o: not (o.is_predefined() or o.is_generic()))
    GENERIC_TYPE = (suite.NamedType, lambda o: o.is_generic())
    FIELD = (suite.CompositeElement, lambda o: True)
    SENSOR = (suite.Sensor, lambda o: True)
    CONSTANT = (suite.Constant, lambda o: isinstance(o.owner, suite.Package))
    ENUM_VALUE = (suite.Constant, lambda o: isinstance(o.owner, suite.Enumeration))
    PARAMETER = (suite.Constant, lambda o: isinstance(o.owner, suite.Operator))
    OPERATOR = (suite.Operator, lambda o: True)
    VARIABLE = (suite.LocalVariable, lambda o: o.is_local() and not o.is_internal())
    INPUT = (suite.LocalVariable, lambda o: o.is_input())
    HIDDEN = (suite.LocalVariable, lambda o: o.is_hidden())
    OUTPUT = (suite.LocalVariable, lambda o: o.is_output())
    SIGNAL = (suite.LocalVariable, lambda o: o.is_signal())
    INTERNAL = (suite.LocalVariable, lambda o: o.is_internal())
    DIAGRAM = (suite.Diagram, lambda o: not isinstance(o, suite.TreeDiagram))
    EQ_SET = (suite.EquationSet, lambda o: True)
    STATE_MACHINE = (suite.StateMachine, lambda o: True)
    STATE = (suite.State, lambda o: True)
    IF_BLOCK = (suite.IfBlock, lambda o: True)
    WHEN_BLOCK = (suite.WhenBlock, lambda o: True)
