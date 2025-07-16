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

"""Implements the LevelOfDepthOfStructures rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))

import scade.model.suite as suite

from ansys.scade.apitools.query import get_leaf_type
from ansys.scade.design_rules.utils.rule import Rule


class LevelOfDepthOfStructures(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0031',
        category='Modelling',
        severity=Rule.REQUIRED,
        parameter='4',
        description=(
            "A SCADE structure type shall contain at most 'parameter-value' "
            'level of sub structures.\n'
            'var.level1.level2.level3'
        ),
        label='Level of Depth of Structures',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.Structure],
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = '') -> int:
        """Get the rule's parameters."""
        if not parameter.isdigit():
            self.set_message(
                f'Parameter for rule is not an integer or lower than zero: {parameter}'
            )
            return Rule.ERROR

        return Rule.OK

    def on_check(self, object_: suite.Object, parameter: str = '') -> int:
        """Return the evaluation status for the input object."""
        assert isinstance(object_, suite.Structure)
        depth = self.get_depth(object_)

        if depth > int(parameter):
            message = f'Level of Depth of structure is too large ({depth} > {parameter})'
            self.set_message(message)
            return Rule.FAILED
        return Rule.OK

    def get_depth(self, structure: suite.Structure) -> int:
        """Return the maximum depth of a structure."""
        max_depth = 0
        for field in structure.elements:
            type_ = get_leaf_type(field.type)
            if isinstance(type_, suite.Structure):
                depth = self.get_depth(type_)
                if depth > max_depth:
                    max_depth = depth

        return max_depth + 1


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    LevelOfDepthOfStructures()
