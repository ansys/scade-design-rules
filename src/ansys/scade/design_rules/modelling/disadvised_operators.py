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

"""Implements the DisadvisedOperators rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class DisadvisedOperators(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0013',
        category='Modelling',
        severity=Rule.ADVISORY,
        parameter='46, 47, 51, 52',
        description=(
            'Specific predefined SCADE operators should not be used: '
            'reverse (46), transpose (47), slice (51), Concatenation (52)'
        ),
        label='Disadvised Operators',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.ExprCall],
            kinds=None,
        )

    def on_start(self, model: suite.Model = None, parameter: str = None) -> int:
        """Get the rule's parameters."""
        self.disadvised_operators = [_.strip() for _ in parameter.split(',')]
        return Rule.OK

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        if str(object_.predef_opr) in self.disadvised_operators:
            container = self.get_closest_annotatable(object_)
            error_msg = 'Disadvised operator used: ' + object_.to_string()
            identifier = object_.to_string()
            self.add_rule_status(container, Rule.FAILED, error_msg, identifier)

        return Rule.NA


if __name__ == '__main__':
    # rule instantiated outside of a package
    DisadvisedOperators()
