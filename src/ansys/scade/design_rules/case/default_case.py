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

"""Implements the DefaultCase rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade.model.suite as suite

import ansys.scade.apitools.expr as expr
from ansys.scade.design_rules.utils.rule import Rule


class DefaultCase(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0012',
        description="In the SCADE model, any 'case' construct shall use the "
        "'default' to catch any abnormal value.",
        label='Case default checked',
        category='case',
        severity=Rule.MANDATORY,
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=False,
            default_param='',
            description=description,
            label=label,
            types=[suite.ExprCall],
            kinds=None,
        )

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        call = expr.accessor(object_)
        if isinstance(call, expr.CaseOp) and not call.default:
            container = self.get_closest_annotatable(object_)
            error_msg = 'Switch without default case.'
            identifier = object_.to_string()
            self.add_rule_status(container, Rule.FAILED, error_msg, identifier)

        return Rule.NA


if __name__ == '__main__':
    # rule instantiated outside of a package
    DefaultCase()
