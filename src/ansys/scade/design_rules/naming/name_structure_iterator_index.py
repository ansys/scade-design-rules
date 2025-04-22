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

"""Implements the NameStructureIteratorIndex rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))

import re

import scade
import scade.model.suite as suite

from ansys.scade.design_rules.utils.command import ParameterParser
from ansys.scade.design_rules.utils.modelling import IR, get_iter_role
from ansys.scade.design_rules.utils.rule import SCK, Rule


class NameStructureIteratorIndex(Rule):
    """Implements the rule interface."""

    # parameter = "index = index"
    def __init__(
        self,
        id='id_0051',
        label='Name structure of iterator index',
        description=(
            'For iterators which use an index (mapi, mapwi, foldi, foldwi, '
            'mapfoldi, mapfoldwi), the input corresponding to the index shall be named'
            " or prefixed by 'index'."
        ),
        category='Naming',
        severity=Rule.REQUIRED,
        parameter='-i index',
        **kwargs,
    ):
        super().__init__(
            id=id,
            label=label,
            description=description,
            category=category,
            severity=severity,
            kinds=[SCK.INPUT, SCK.HIDDEN],
            has_parameter=True,
            default_param=parameter,
            **kwargs,
        )
        self.index_regexp = None

    def on_start(self, model: suite.Model, parameter: str) -> int:
        """Get the rule's parameters."""
        parameter = parameter.replace('index=', '-i ') if parameter else ''
        parser = ParameterParser(prog='')
        parser.add_argument('-i', '--index', help='Regular expression for index', required=True)
        options = parser.parse_command(parameter)
        if not options:
            message = parser.message
        else:
            self.index_regexp = options.index
            return Rule.OK

        self.set_message(message)
        scade.output(message + '\n')
        return Rule.ERROR

    def on_check_ex(self, variable: suite.LocalVariable, parameter: str = None) -> int:
        """
        Return the evaluation status for the input object.

        Retrieve the variable's roles for all instances of its operator, fail when:

        * the variable is used as index and does not match the index
          regular expression
        """
        failure = False
        name = variable.name

        # collect all roles in a set to avoid redundant failures
        roles = {get_iter_role(variable, call) for call in variable.operator.expr_calls}
        lines = []
        for role in roles:
            if role == IR.INDEX:
                if not re.fullmatch(self.index_regexp, name):
                    failure = True
                    lines.append(f'The name does not match the index expression {self.index_regexp}')

        if failure:
            self.set_message(',\n'.join(lines))
            return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    NameStructureIteratorIndex()
