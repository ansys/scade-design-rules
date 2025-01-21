# -*- coding: utf-8 -*-

# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Implements the EnumTypeNamePrefix rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

import re

import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import SCK, Rule


class EnumTypeNamePrefix(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0018',
        category='Naming',
        severity=Rule.REQUIRED,
        parameter='Type',
        description='Checks if the values of a given Enumeration are prefixed with its name',
        label='Enumeration literal prefix check',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=None,
            kinds=[SCK.ENUM_VALUE],
        )

    def on_check_ex(self, object: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        enum_name = object.owner.owner.name  # the owner is the NamedType for this enum
        prefix = re.sub(
            parameter + '$', '', enum_name
        )  # remove parameter string from end of the name+
        # scade.output(object.name + "\n")
        if not object.name.startswith(prefix):
            self.set_message(
                'Enumeration literal does not start with ' + prefix + '(Value of ' + enum_name + ')'
            )
            return Rule.FAILED

        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    EnumTypeNamePrefix()
