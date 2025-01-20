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

"""Implements the LocalNameUniqueness rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade.model.suite as suite
from scade.model.suite.visitors import Visit

from ansys.scade.design_rules.utils.rule import Rule


class _GatherLocalVariables(Visit):
    """Dictionary of local variables, indexed by name."""

    def __init__(self, operator: suite.Operator):
        self.variables = {}
        self.visit(operator)

    def visit_local_variable(self, local_variable: suite.LocalVariable, *args):
        if not local_variable.is_internal():
            self.variables.setdefault(local_variable.name, []).append(local_variable)


class LocalNameUniqueness(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0038',
        label='Local name uniqueness',
        description='The names of local variables and signals shall be unique within an operator.',
        category='Readability',
        severity=Rule.ADVISORY,
        **kwargs,
    ):
        # The rule applies to local variables but the computations are done at the operator level
        super().__init__(
            id=id,
            label=label,
            description=description,
            category=category,
            severity=severity,
            types=[suite.Operator, suite.LocalVariable],
            has_parameter=False,
            **kwargs,
        )
        self.cache_variables = {}

    def before_checking_subtree(self, object_: suite.Object, parameter: str = None) -> int:
        """Cache all the local variables when object_ is an operator."""
        if isinstance(object_, suite.Operator):
            self.cache_variables = _GatherLocalVariables(object_).variables
        return Rule.OK

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        # default
        status = Rule.OK
        if isinstance(object_, suite.LocalVariable) and not object_.is_internal():
            variables = self.cache_variables[object_.name]
            if len(variables) > 1:
                message = '%s: Not unique name' % object_.name
                self.set_message(message)
                status = Rule.FAILED
        return status


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    LocalNameUniqueness()
