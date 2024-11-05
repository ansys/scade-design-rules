# -*- coding: utf-8 -*-

# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
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

# list all the presentable elements of the loaded projects

import scade
import scade.model.suite as suite
from scade.model.suite import get_roots as get_sessions
from scade.model.suite.visitors import Visit


def outputln(text):
    scade.output(text + '\n')


class ListElements(Visit):
    def __init__(self, model: suite.Model):
        self.visit(model)

    def visit_presentable(self, presentable: suite.Presentable, *args):
        pe = presentable.presentation_element
        if pe and isinstance(pe.diagram, suite.NetDiagram):
            outputln("        ('%s', _ERROR)," % presentable.get_full_path())

    def visit_edge(self, edge: suite.Edge, *args):
        outputln("        ('%s', _ERROR)," % edge.left_var.get_full_path())


for session in get_sessions():
    ListElements(session.model)
