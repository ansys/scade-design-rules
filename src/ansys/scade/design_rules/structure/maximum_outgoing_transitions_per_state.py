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

"""Implements the MaximumOutgoingTransitionsPerState rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))

import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class MaximumOutgoingTransitionsPerState(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0072',
        category='Structuring',
        severity=Rule.REQUIRED,
        parameter='7',
        label='Maximum outgoing transitions per state',
        description=(
            "Maximum outgoing transitions per state.\nParameter: maximum value: e.g.: '7'"
        ),
        metric_id: str = 'id_0125',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.State],
            kinds=None,
            metric_ids=[metric_id],
        )
        self.metric_id = metric_id

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        if not parameter.isdigit():
            self.set_message(
                f'Parameter for rule is not an integer or lower than zero: {parameter}'
            )
            return Rule.ERROR

        return Rule.OK

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        count = self.get_metric_result(object_, self.metric_id)

        if count > int(parameter):
            self.set_message(f'Too many outgoing transitions per state ({count} > {parameter})')
            return Rule.FAILED

        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    MaximumOutgoingTransitionsPerState()
