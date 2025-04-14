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

"""Implements the EnumDefinitionElementsOrder rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.modelling import get_enum_value
from ansys.scade.design_rules.utils.rule import Rule


def is_asc(values: list):
    """Return whether the values are in ascending order."""
    return all(values[i + 1] > values[i] for i in range(len(values) - 1))


def is_desc(values: list):
    """Return whether the values are in descending order."""
    return all(values[i + 1] < values[i] for i in range(len(values) - 1))


class EnumDefinitionElementsOrder(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0016',
        category='Types',
        label='Enumeration definition elements order',
        severity=Rule.ADVISORY,
        parameter='order=asc,by=name',
        description=(
            'Checks if the order of definition elements of enumerations is '
            'ascending (``order=asc``) or descending (``order=desc``).\n'
            'The elements are ordered by name (``by=name``) or by value '
            '(``by=value``).'
        ),
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.Enumeration],
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        # whether all enumeration values must have a kcg pragma value
        self.strict = False

        d = self.parse_values(parameter)
        if d is None:
            message = f"'{parameter}': parameter syntax error"
        else:
            order = d.get('order')
            by = d.get('by')
            if not order:
                message = f"'{parameter}': missing 'order' value"
            elif not by:
                message = f"'{parameter}': missing 'by' value"
            else:
                self.order = order
                self.by = by
                return Rule.OK

        self.set_message(message)
        return Rule.ERROR

    def on_check(self, object: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        if self.by == 'name':
            values = [_.name for _ in object.values]
        else:
            values = []
            last_value = -1
            missing_enum_values = []
            for value in object.values:
                v = get_enum_value(value)
                if v == -1:
                    missing_enum_values.append(value.name)
                    # C, C++, C#... semantic
                    v = last_value + 1
                last_value = v
                values.append(v)

            if self.strict and len(missing_enum_values) > 0:
                self.set_message(
                    f"Missing Enum values. Cannot check for order: {', '.join(missing_enum_values)}"
                )
                return Rule.FAILED

        if self.order == 'asc' and not is_asc(values):
            self.set_message('Value list is not in ascending order')
            return Rule.FAILED
        elif self.order == 'desc' and not is_desc(values):
            self.set_message('Value list is not in descending order')
            return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    EnumDefinitionElementsOrder()
