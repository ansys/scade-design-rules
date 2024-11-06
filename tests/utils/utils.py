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

import scade.model.suite as suite


# get_object_from_path does not find equations sets nor diagrams
def get_equation_set_or_diagram_from_path(model: suite.Model, path: str) -> suite.Annotable:
    tokens = path.rstrip('/').split('/')
    tokens = path.rstrip('/').split('/')
    # 2 tokens for a diagram, 3 for an equation set
    assert len(tokens) > 1
    sub_tokens = tokens[1].split(':')
    sub_path = '/'.join([tokens[0], ':'.join(sub_tokens[:-1])])
    datadef = model.get_object_from_path(sub_path)

    for diagram in datadef.diagrams:
        if diagram.name == sub_tokens[-1]:
            assert isinstance(diagram, suite.Diagram)
            if len(tokens) == 2:
                return diagram
            assert len(tokens) == 3
            for eqset in diagram.equation_sets:
                if eqset.name == tokens[-1]:
                    return eqset
    # not found
    return None


# 2023 R1 ->
# return a dictionary of all the links of a project
def get_project_requirement_ids(trace):
    links = {}
    if trace:
        for link in trace.traceability_links:
            links.setdefault(link.source.identifier, []).append(link.target.identifier)
    return links
