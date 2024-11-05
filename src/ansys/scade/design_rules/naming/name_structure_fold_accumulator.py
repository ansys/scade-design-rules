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

"""Implements the NameStructureFoldAccumulator rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

import re

import scade
import scade.model.suite as suite

from ansys.scade.design_rules.utils.modelling import IR, get_iter_role
from ansys.scade.design_rules.utils.rule import SCK, Rule


class NameStructureFoldAccumulator(Rule):
    """Implements the rule interface."""

    # parameter = "in = acc.*In, out = acc.*Out, strict =False"
    def __init__(
        self,
        id='id_0049',
        label='Name structure of accumulator inputs/outputs',
        description=(
            'For the operators iterated with fold constructs (fold, foldi, foldw, '
            'foldwi, mapfold, mapfoldi, mapfoldw, mapfoldwi):\n'
            "* The accumulators are defined by a name prefixed by 'acc'.\n"
            '* The input/output variables of an accumulator shall be discriminated by '
            "  the suffix 'In' for the inputs and 'Out' for the outputs.\n"
            '* The input and output names of the accumulators match.\n'
            '\n'
            'The parameter allows specifying a regular expression for input and output names.\n'
            "For example: 'in=acc(.*)In, out=acc(.*)Out'. The parenthesis identifies the common "
            'part of both names that must match.\n'
            '\n'
            'When strict is set, the rules verifies the names are not used for variables '
            'which are not accumulators.'
        ),
        category='Naming',
        severity=Rule.REQUIRED,
        parameter='in=acc(.*)In, out=acc(.*)Out',
        **kwargs,
    ):
        super().__init__(
            id=id,
            label=label,
            description=description,
            category=category,
            severity=severity,
            types=[],
            kinds=[SCK.INPUT, SCK.HIDDEN, SCK.OUTPUT],
            has_parameter=True,
            default_param=parameter,
            **kwargs,
        )
        self.in_regexp = None
        self.out_regexp = None
        self.strict = False

    def on_start(self, model: suite.Model, parameter: str) -> int:
        """Get the rule's parameters."""
        assert model is not None

        d = self.parse_values(parameter)
        if d is None:
            message = "'%s': parameter syntax error" % parameter
        else:
            self.in_regexp: str = d.get('in', '')
            self.out_regexp: str = d.get('out', '')
            strict = d.get('strict')
            self.strict = strict is not None and (strict.lower() == 'true' or strict == '1')
            if not self.in_regexp:
                message = "'%s': missing 'in' value" % parameter
            elif not self.out_regexp:
                message = "'%s': missing 'out' value" % parameter
            else:
                return Rule.OK

        self.set_message(message)
        scade.output(message + '\n')
        return Rule.ERROR

    def on_check_ex(self, variable: suite.LocalVariable, parameter: str = None) -> int:
        """
        Return the evaluation status for the input object.

        Retrieve the variable's roles for all instances of its operator and fail when:

        * The variable is an input (resp. output) accumulator and does not
          match the in (resp. out) regular expression
        * The variable is not an accumulator and matches one of the in/out
          regular expressions
        """
        failure = False
        name = variable.name

        # collect all roles in a set to avoid redundant failures
        operator = variable.operator
        roles = {get_iter_role(variable, call) for call in operator.expr_calls}
        lines = []
        for role in roles:
            if role == IR.ACC_IN:
                m = re.fullmatch(self.in_regexp, name)
                if not m:
                    failure = True
                    lines.append(
                        'The name does not match the input accumulator expression %s'
                        % self.in_regexp
                    )
                else:
                    groups = m.groups()
                    if groups:
                        base_name = groups[0]
                        # search the operator for a corresponding input
                        for input in operator.outputs:
                            m = re.fullmatch(self.out_regexp, input.name)
                            if m and m.groups() and m.groups()[0] == base_name:
                                # match found
                                break
                        else:
                            failure = True
                            lines.append(
                                'Matching output accumulator not found: %s' % variable.name
                            )
            elif role == IR.ACC_OUT:
                m = re.fullmatch(self.out_regexp, name)
                if not m:
                    failure = True
                    lines.append(
                        'The name does not match the output accumulator expression %s'
                        % self.out_regexp
                    )
                else:
                    groups = m.groups()
                    if groups:
                        base_name = groups[0]
                        # search the operator for a corresponding input
                        for input in operator.inputs + operator.hiddens:
                            m = re.fullmatch(self.in_regexp, input.name)
                            if m and m.groups() and m.groups()[0] == base_name:
                                # match found
                                break
                        else:
                            failure = True
                            lines.append(
                                'Matching input accumulator not found for %s' % variable.name
                            )
            else:
                if self.strict and (
                    re.fullmatch(self.in_regexp, name) or re.fullmatch(self.out_regexp, name)
                ):
                    failure = True
                    lines.append('The variable is not used as an accumulator')

        if failure:
            self.set_message(',\n'.join(lines))
            return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    NameStructureFoldAccumulator()
