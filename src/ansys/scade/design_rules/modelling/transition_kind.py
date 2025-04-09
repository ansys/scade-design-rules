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

"""Implements the TransitionKind rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class TransitionKind(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0085',
        category='Modelling',
        severity=Rule.REQUIRED,
        parameter='nomix',
        description=(
            'Check that all transitions of a state machine are of the same kind, '
            'are all strong or are all weak transitions.\n'
            "parameter: strong, weak, nomix: e.g.: 'nomix'"
        ),
        label='Transition Kind',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.StateMachine],
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        if parameter not in {'strong', 'weak', 'nomix'}:
            self.set_message('Wrong parameter: ' + parameter)
            return Rule.ERROR

        return Rule.OK

    def on_check(self, object: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        violated = False

        weaks = 0
        strongs = 0
        for state in object.states:
            for transition in state.outgoings:
                if transition.transition_kind == 'Weak' or transition.transition_kind == 'Synchro':
                    weaks += 1
                elif transition.transition_kind == 'Strong':
                    strongs += 1

        message = ''
        if parameter == 'nomix':
            if weaks > 0 and strongs > 0:
                message = 'State with mix of strong and weak transitions found.'
                violated = True
        if parameter == 'strong':
            if weaks > 0:
                message = 'State with weak transitions found.'
                violated = True
        if parameter == 'weak':
            if strongs > 0:
                message = 'State with strong transitions found.'
                violated = True

        if violated:
            self.set_message(message)
            return Rule.FAILED

        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    TransitionKind()
