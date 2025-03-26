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

# list the equations of the model for the test cases of test_eq_in_eq_set.py

import scade
from scade.model.suite import get_roots as get_sessions
from scade.model.suite.visitors import Visit


def outputln(text):
    scade.output(text + '\n')


class ListEquations(Visit):
    def __init__(self):
        self.index = 0

    def visit_equation(self, equation, *args):
        super().visit_equation(equation, *args)
        outputln("    (%2d, '%s', )," % (self.index, equation.get_full_path()))
        self.index += 1

    def visit_if_node(self, if_action, *args):
        super().visit_if_node(if_action, *args)
        outputln("    (%2d, '%s', )," % (self.index, if_action.get_full_path()))
        self.index += 1

    def visit_when_branch(self, when_branch, *args):
        super().visit_when_branch(when_branch, *args)
        outputln("    (%2d, '%s', )," % (self.index, when_branch.get_full_path()))
        self.index += 1

    def visit_state(self, state, *args):
        super().visit_state(state, *args)
        outputln("    (%2d, '%s', )," % (self.index, state.get_full_path()))
        self.index += 1

    def visit_transition(self, transition, *args):
        super().visit_transition(transition, *args)
        outputln("    (%2d, '%s', )," % (self.index, transition.get_full_path()))
        self.index += 1


for session in get_sessions():
    ListEquations().visit(session.model)
