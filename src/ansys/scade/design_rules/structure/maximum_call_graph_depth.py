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

"""Implements the MaximumCallGraphDepth rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))

from typing import List

import scade
import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class MaximumCallGraphDepth(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0039',
        category='Structuring',
        severity=Rule.REQUIRED,
        parameter='depth=7,visibility=Public',
        description=(
            "Maximum depth of the call graph shall not exceed 'parameter'.\n"
            'Check is performed on only public or all operators. '
            'Parameter: depth=:maximum value, visibility=Public,ALL '
            '(e.g.: depth=7,visibility=Public)'
        ),
        label='Maximum call graph depth',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.Operator],
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        d = self.parse_values(parameter)
        if d is None:
            message = f"'{parameter}': parameter syntax error"
        else:
            depth = d.get('depth')
            visibility = d.get('visibility')
            if not depth:
                message = f"'{parameter}': missing 'depth' value"
            elif not visibility:
                message = f"'{parameter}': missing 'visibility' value"
            else:
                if not depth.isdecimal():
                    message = f"'{depth}' is not a number"
                else:
                    self.depth = int(depth)
                    self.visibility = visibility
                    return Rule.OK

        self.set_message(message)
        scade.output(message + '\n')
        return Rule.ERROR

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        if self.visibility == 'Public':
            if object_.visibility != 'Public':
                return Rule.NA

        call_graph_max = self._get_max_call_graph(object_)
        level = len(call_graph_max)
        if level > self.depth:
            self.set_message(
                f'Call graph depth too high ({level} > {self.depth}): {".".join(call_graph_max)}'
            )
            return Rule.FAILED

        return Rule.OK

    def _get_max_call_graph(self, operator: suite.Operator) -> List[str]:
        max_sub_call_graph = []
        for sub_op in operator.called_operators:
            sub_call_graph = self._get_max_call_graph(sub_op)
            if len(sub_call_graph) > len(max_sub_call_graph):
                max_sub_call_graph = sub_call_graph
        return [operator.name] + max_sub_call_graph


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    MaximumCallGraphDepth()
