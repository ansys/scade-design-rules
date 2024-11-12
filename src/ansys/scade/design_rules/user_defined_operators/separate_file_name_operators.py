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

"""Implements the SeparateFileNameOperators rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class SeparateFileNameOperators(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0082',
        category='User-Defined Operators',
        parameter='type=dechecked',
        label='All operators should have the option Separate File Name checked or unchecked',
        severity=Rule.ADVISORY,
        description=(
            'This rule checks that all operators have the option '
            'Separate File Name checked (``type=checked``) or '
            'unchecked ``type=dechecked``).'
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
            types=[suite.Operator],
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        d = self.parse_values(parameter)
        if d is None:
            message = "'%s': parameter syntax error" % parameter
        else:
            type = d.get('type')
            if type is None:
                message = "'%s': missing 'type' value" % parameter
            else:
                self.type = type
                return Rule.OK

        self.set_message(message)
        return Rule.ERROR

    def on_check(self, object: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        if self.type == 'checked':
            if object.storage_unit is None:
                self.set_message("Option 'Separate File Name' should be checked for this Operator!")
                return Rule.FAILED
        else:
            if object.storage_unit is not None:
                self.set_message(
                    "Option 'Separate File Name' should be de-checked for this Operator!"
                )
                return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':
    # rule instantiated outside of a package
    SeparateFileNameOperators()
