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

"""Implements the NameStructureType rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import scade
import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class NameStructureType(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0053',
        category='Naming',
        label='Type Name Structure',
        severity=Rule.REQUIRED,
        parameter='prefix=,suffix=_t',
        description=('Type shall start/end with specific characters _t, t_, Type_.'),
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.NamedType],
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        d = self.parse_values(parameter)
        if d is None:
            message = f"'{parameter}': parameter syntax error"
        else:
            prefix = d.get('prefix')
            suffix = d.get('suffix')
            if prefix is None:
                message = f"'{parameter}': missing 'prefix' value"
            elif suffix is None:
                message = f"'{parameter}': missing 'suffix' value"
            else:
                self.prefix = prefix
                self.suffix = suffix
                return Rule.OK

        self.set_message(message)
        scade.output(message + '\n')
        return Rule.ERROR

    def on_check(self, object: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        failure = False
        text = []
        name = object.name

        if not name.endswith(self.suffix):
            failure = True
            text.append(f'Type name does not end with {self.suffix}')

        if not name.startswith(self.prefix):
            failure = True
            text.append(f'Type name does not start with {self.prefix}')

        if failure:
            self.set_message(', '.join(text))
            return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    NameStructureType()
