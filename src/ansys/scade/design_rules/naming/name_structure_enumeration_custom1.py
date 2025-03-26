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

"""Implements the NameStructureEnumerationCustom1 rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class NameStructureEnumerationCustom1(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0109',
        category='Naming',
        severity=Rule.REQUIRED,
        parameter='Type',
        description=(
            'The Model Designer shall prefix enumeration literal with the '
            "enumeration type name (excluding the 'Type' suffix).\n"
            'parameter: suffix'
        ),
        label='Enumeration Name Structure Custom1',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.Constant],
            kinds=None,
        )

    def on_check(self, object: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        if not isinstance(object.owner, suite.Enumeration):
            return Rule.OK

        name = object.name
        enumeration_type = object.type
        enum_base_name = enumeration_type.name.rstrip(parameter)

        if name.startswith(enumeration_type.name):
            self.set_message(name + ' starts with full type name ' + enumeration_type.name)
            return Rule.FAILED
        elif not name.startswith(enum_base_name):
            self.set_message(name + ' does not start with ' + enum_base_name)
            return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    NameStructureEnumerationCustom1()
