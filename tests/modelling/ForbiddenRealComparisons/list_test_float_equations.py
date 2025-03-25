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

# list all the equations of the operator IsFloat with the expected status

import scade
import scade.model.suite as suite
from scade.model.suite import get_roots as get_sessions


def outputln(text):
    scade.output(text + '\n')


for session in get_sessions():
    operator = session.model.get_object_from_path('P::IsFloat/')
    assert operator
    for diagram in operator.diagrams:
        status = diagram.name == 'Yes'  # else 'No'
        for pe in diagram.presentation_elements:
            if not isinstance(pe, suite.EquationGE):
                continue
            eq = pe.equation
            if len(eq.lefts) != 1 or eq.lefts[0].name == '_':
                continue

            outputln("    ('%s', %s)," % (eq.get_full_path(), status))
