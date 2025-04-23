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

"""Implements the EqInEqSet rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class EqInEqSet(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0019',
        label='Equation or branch belong to at least one equation set',
        description=(
            'An equation or a branch shall belong to at least one equation set except '
            'following uses cases:\n'
            "* The element is text: textual diagram, transition's action, textual state, etc.\n"
            '* The element is in a state without diagram (Embedded state)'
        ),
        category='Traceability',
        severity=Rule.ADVISORY,
        **kwargs,
    ):
        super().__init__(
            id=id,
            label=label,
            description=description,
            category=category,
            severity=severity,
            types=[suite.Equation, suite.WhenBranch, suite.IfNode],
            has_parameter=False,
            **kwargs,
        )

    def on_check(self, presentable: suite.Presentable, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        state = self.get_owning_state(presentable)
        if state and not state.diagrams:
            status = Rule.OK
        else:
            pe = presentable.presentation_element
            if not pe or isinstance(pe.diagram, suite.TextDiagram):
                status = Rule.OK
            else:
                if presentable.equation_sets:
                    status = Rule.OK
                else:
                    status = Rule.FAILED
                    kind = 'equation' if isinstance(presentable, suite.Equation) else 'branch'
                    message = 'the {} {} shall belong to at least one equation set'
                    self.set_message(message.format(kind, presentable.get_full_path()))
        return status

    def get_owning_state(self, object_: suite.Object) -> suite.State:
        """Return the state owning the item, directly or not, if any."""
        owner = object_.owner
        while not isinstance(owner, suite.Operator):
            if isinstance(owner, suite.State):
                return owner
            owner = owner.owner
        return None


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    EqInEqSet()
