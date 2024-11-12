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

"""Implements the ElementNamesUniqueInProject rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import SCK, Rule


class ElementNamesUniqueInProject(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0124',
        category='Naming',
        description=(
            'The name of an element shall not be used for any other element (of the same kind) '
            'in the entire project (+ libraries)'
        ),
        label='The name of an element shall not be used for any other element.',
        severity=Rule.REQUIRED,
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=False,
            default_param='',
            description=description,
            label=label,
            types=[],
            kinds=[SCK.CONSTANT],
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Cache the constants."""
        self.constants = {}
        for constant in model.all_constants:
            self.constants.setdefault(constant.name, []).append(constant)
        return Rule.OK

    def on_check_ex(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        constants = self.constants[object_.name]
        paths = [_.get_full_path() for _ in constants if _ != object_]

        if paths:
            self.set_message('Element name also used here: ' + ', '.join(paths))
            return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':
    # rule instantiated outside of a package
    ElementNamesUniqueInProject()
