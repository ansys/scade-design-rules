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

"""Implements the EqInEqSetOrNet rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import scade.model.suite as suite

from ansys.scade.design_rules.traceability.eq_in_eq_set import EqInEqSet
from ansys.scade.design_rules.utils.rule import Rule


class EqInEqSetOrNet(EqInEqSet):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0094',
        description=(
            'An equation or a branch shall belong to at least one equation set '
            'except following uses cases:\n'
            "* The element is text: textual diagram, transition's action, textual state, etc.\n"
            '* The element is in a state without diagram (Embedded state)\n'
            "* The element's diagram has no equation sets"
        ),
        **kwargs,
    ):
        super().__init__(id=id, description=description, **kwargs)

    def on_check(self, presentable: suite.Presentable, parameter: str = '') -> int:
        """Return the evaluation status for the input object."""
        pe = presentable.presentation_element
        if pe and isinstance(pe.diagram, suite.NetDiagram) and not pe.diagram.equation_sets:
            status = Rule.OK
        else:
            status = super().on_check(presentable, parameter)
        return status


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    EqInEqSetOrNet()
