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

"""Implements the NameStructurePackage rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.naming import is_pascal_case
from ansys.scade.design_rules.utils.rule import SCK, Rule


class NameStructurePackage(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0052',
        label='Package name',
        description='Package names shall be short (at most 10 characters for example).',
        category='Naming',
        severity=Rule.REQUIRED,
        parameter='10',
        **kwargs,
    ):
        # default value for kinds when neither types nor kinds is specified
        super().__init__(
            id=id,
            label=label,
            description=description,
            category=category,
            severity=severity,
            kinds=[SCK.PACKAGE],
            has_parameter=True,
            default_param=parameter,
            **kwargs,
        )

    def on_check_ex(self, object_: suite.Object, parameter: str = '') -> int:
        """Return the evaluation status for the input object."""
        name = object_.name
        length = int(parameter) if parameter else 0
        if len(name) > length:
            message = f'{name}: The name is longer than {length:.0f}'
            self.set_message(message)
            status = Rule.FAILED
        elif not is_pascal_case(name):
            status = Rule.FAILED
            message = f'{name}: The name shall be composed of a sequence of words'
            self.set_message(message)
        else:
            status = Rule.OK
        return status


if __name__ == '__main__':  # pragma: no cover
    NameStructurePackage()
