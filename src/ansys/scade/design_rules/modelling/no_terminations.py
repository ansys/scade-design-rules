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

"""Implements the NoTerminations rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

import scade.model.suite as suite

from ansys.scade.apitools.expr import Eck
from ansys.scade.design_rules.utils.rule import Rule


class NoTerminations(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0063',
        category='Modelling',
        severity=Rule.ADVISORY,
        parameter='NOIT',
        description=(
            'Terminations should not be used.\n'
            "parameter: 'ALL': all, 'NOIT: do not report terminations at iterator outputs'"
        ),
        label='No terminations',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.Equation],
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        if parameter not in ['ALL', 'NOIT']:
            self.set_message('Wrong parameter')
            return Rule.ERROR

        return Rule.OK

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        if len(object_.lefts) != 1 or object_.lefts[0].name != '_':
            # not a terminator
            return Rule.NA

        # report the source equation, with the pin number, to allow
        # the equation to be located in the graphics
        local_var_connecting_it_and_termination = object_.right.reference
        prev_eqs = local_var_connecting_it_and_termination.definitions
        if not prev_eqs:
            # semantic error, reporting useless and not easy
            return Rule.NA

        # consider the first source equation
        # (more than one is unlikely but possible with textual diagrams and control blocks)
        violated = False
        prev_eq = prev_eqs[0]
        index_pos_of_var = prev_eq.lefts.index(local_var_connecting_it_and_termination)
        assert index_pos_of_var == local_var_connecting_it_and_termination.left_range
        right = prev_eq.right
        if parameter == 'NOIT' and isinstance(right, suite.ExprCall):
            # ignore 'exit index' and 'exit condition' outputs
            if right.modifier:
                if Eck(right.modifier.predef_opr) in [
                    Eck.MAPFOLDW,
                    Eck.MAPFOLDWI,
                ]:
                    violated = index_pos_of_var > 1
                elif Eck(right.modifier.predef_opr) in [
                    Eck.MAPW,
                    Eck.MAPWI,
                    Eck.FOLDW,
                    Eck.FOLDWI,
                ]:
                    violated = index_pos_of_var > 0
            else:
                violated = True
        else:
            # no exceptions
            violated = True

        if violated:
            error_msg = 'Termination found at output %d' % index_pos_of_var
            identifier = str(index_pos_of_var)
            self.add_rule_status(prev_eq, Rule.FAILED, error_msg, identifier)

        return Rule.NA


if __name__ == '__main__':
    # rule instantiated outside of a package
    NoTerminations()
