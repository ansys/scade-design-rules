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

"""Implements the StatemachineHasDefaultState rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade.model.suite as suite

from ansys.scade.apitools.prop import get_pragma_tool_text
from ansys.scade.design_rules.utils.rule import Rule


class StatemachineHasDefaultState(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0105',
        category='case',
        label='State machine default checked',
        severity=Rule.MANDATORY,
        description=(
            "In the SCADE model, each state machine shall use the 'default' "
            'for one state to catch any abnormal value.'
        ),
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=False,
            default_param='',
            description=description,
            label=label,
            types=[suite.StateMachine],
            kinds=None,
        )

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        if all((get_pragma_tool_text(_, 'kcg', 'default') is None for _ in object_.states)):
            self.set_message('State machine without default state.')
            return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':
    # rule instantiated outside of a package
    StatemachineHasDefaultState()
