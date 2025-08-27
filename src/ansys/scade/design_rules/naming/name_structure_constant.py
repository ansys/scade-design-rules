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

"""Implements the NameStructureConstant rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class NameStructureConstant(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0046',
        category='Naming',
        severity=Rule.REQUIRED,
        parameter='_c',
        description=(
            'Constant shall be in uppercase letters and start or end with specific '
            'character _c, c_, Const_.'
        ),
        label='Constant Name Structure',
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

    def on_check(self, object: suite.Object, parameter: str = '') -> int:
        """Return the evaluation status for the input object."""
        if isinstance(object.owner, suite.Enumeration):
            return Rule.OK

        failure = False
        text = ''
        name = object.name

        if parameter.startswith('_'):
            if not name.endswith(parameter):
                failure = True
                text += f'Constant name does not end with {parameter}, '

        elif parameter.endswith('_'):
            if not name.startswith(parameter):
                failure = True
                text += f'Constant name does not start with {parameter}, '

        if not name.replace(parameter, '').isupper():
            failure = True
            text += 'Constant is not in capital letters, '

        if failure:
            text = text[:-2]
            self.set_message(text)
            return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    NameStructureConstant()
