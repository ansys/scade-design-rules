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

"""Implements the NoPointerBranch rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import re
from typing import Dict, Optional

import scade.model.suite as suite

from ansys.scade.design_rules.utils.command import ParameterParser
from ansys.scade.design_rules.utils.rule import Rule


class NoPointerBranch(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0091',
        label='Pointer flows must not branch',
        description='A flow, which type is a pointer, shall not be used more than once in a scope.',
        category='Modelling',
        severity=Rule.ADVISORY,
        parameter='-t Ptr.*',
        **kwargs,
    ):
        super().__init__(
            id=id,
            label=label,
            description=description,
            category=category,
            severity=severity,
            types=[suite.LocalVariable],
            has_parameter=True,
            default_param=parameter,
            **kwargs,
        )
        self.types_regexp = ''
        # cache for pointer types
        self.cache_types: Dict[suite.Type, Optional[bool]] = {}

    def on_start(self, model: suite.Model, parameter: str = '') -> int:
        """Get the rule's parameters."""
        # minimal level of backward compatibility
        parameter = parameter.replace('types=', '-t ') if parameter else ''
        parser = ParameterParser(prog='')
        parser.add_argument('-t', '--type', metavar='<type>', help='pointer type', required=True)
        options = parser.parse_command(parameter)
        if not options:
            self.set_message(parser.message)
            return Rule.ERROR

        self.types_regexp = options.type
        return Rule.OK

    def on_check(self, variable: suite.LocalVariable, parameter: str = '') -> int:
        """Return the evaluation status for the input object."""
        if self.is_pointer_type(variable.type):
            # must have one use per scope
            scopes = {_.get_scope() for _ in variable.expr_ids}
            if len(scopes) != len(variable.expr_ids):
                message = f'Illegal branch for {variable.name}'
                self.set_message(message)
                return Rule.FAILED

        return Rule.OK

    def is_pointer_type(self, t: suite.Type) -> bool:
        """Return whether the type is a pointer."""
        is_pointer = self.cache_types.get(t)
        if is_pointer is None:
            if isinstance(t, suite.Table):
                is_pointer = self.is_pointer_type(t.type)
            elif isinstance(t, suite.Structure):
                is_pointer = any(self.is_pointer_type(e.type) for e in t.elements)
            elif isinstance(t, suite.NamedType):
                is_pointer = re.fullmatch(
                    self.types_regexp, t.name
                ) is not None or self.is_pointer_type(t.type)
            else:
                is_pointer = False
        self.cache_types[t] = is_pointer
        return is_pointer


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    NoPointerBranch()
