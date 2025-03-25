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

"""Implements the NoAnonymousType rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import scade
import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import SCK, Rule


class NoAnonymousType(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0122',
        label='No anonymous type in the interface',
        description=(
            'Only named types shall be used in root operator / imported operator '
            'interfaces. Anonymous types (example int^3) shall be avoided.\n'
            'The rule applies to all the root operators, or the root operators '
            'of the specified configuration.'
        ),
        category='Modelling',
        severity=Rule.ADVISORY,
        parameter='configuration=',
        **kwargs,
    ):
        super().__init__(
            id=id,
            label=label,
            description=description,
            category=category,
            severity=severity,
            kinds=[SCK.INPUT, SCK.HIDDEN, SCK.OUTPUT],
            has_parameter=True,
            default_param=parameter,
            **kwargs,
        )
        self.roots = None

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        # restore the default values
        self.roots = None
        # the parameters are optional
        d = self.parse_values(parameter) if parameter else {}
        if d is None:
            message = "'%s': parameter syntax error" % parameter
        else:
            name = d.get('configuration')
            if name:
                # get the project associated to the model
                project = model.project
                configuration = project.find_configuration(name)
                if configuration:
                    self.roots = project.get_tool_prop_def(
                        'GENERATOR', 'ROOTNODE', [], configuration
                    )
            # no error
            return Rule.OK
        self.set_message(message)
        scade.output(message + '\n')
        return Rule.ERROR

    def on_check_ex(self, variable: suite.LocalVariable, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        # local variable must be an io
        if not self._is_root(variable.operator):
            return Rule.NA
        if not isinstance(variable.type, suite.NamedType):
            self.set_message(
                'The type %s shall not be anonymous'
                % (variable.type.to_string() if variable.type else '<null>')
            )
            return Rule.FAILED
        # check the sub types
        for type_ in variable.type.used_types:
            # if a type is anonymous, its owner swhall be a named type
            if isinstance(type_, suite.Structure):
                if not isinstance(type_.owner, suite.NamedType):
                    self.set_message(
                        'The type %s shall not contain anonymous structure'
                        % variable.type.to_string()
                    )
                    return Rule.FAILED
            elif isinstance(type_, suite.Table):
                # matrix accepted
                if not isinstance(type_.owner, suite.NamedType) and not isinstance(
                    type_.owner, suite.Table
                ):
                    self.set_message(
                        'The type %s shall not contain anonymous array' % variable.type.to_string()
                    )
                    return Rule.FAILED

        return Rule.OK

    def _is_root(self, operator: suite.Operator) -> bool:
        # no configuration specified, consider any root operator
        # which is not polymorphic nor parameterized by size
        if operator.parameters or operator.typevars:
            return False
        return (
            operator.is_imported()
            or not operator.expr_calls
            # configuration specified: consider its root operators
            and (not self.roots or operator.get_full_path().strip('/') in self.roots)
        )


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    NoAnonymousType()
