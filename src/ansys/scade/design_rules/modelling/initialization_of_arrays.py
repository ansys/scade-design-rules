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

"""Implements the InitializationOfArrays rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class InitializationOfArrays(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0029',
        category='Modelling',
        severity=Rule.REQUIRED,
        description=(
            'If all elements of an array are identical the initialization shall be '
            'done like this: value ^size\n'
            "Note: An initialization such as ' ', ' ', ' ', ... "
            "leads to more memory usage than ' ' ^n."
        ),
        label='Initialization of Arrays',
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
        violated = False
        ref_value = None

        # 41 = SC_ECK_BLD_VECTOR
        if object_.predef_opr == 41:
            assert object_.parameters
            ref_value = self.get_expr_value(object_.parameters[0])
            for parameter in object_.parameters[1:]:
                value = self.get_expr_value(parameter)
                # compare to all other elements
                if ref_value != value:
                    break
            else:
                violated = True

        if violated:
            assert ref_value
            container = self.get_closest_annotatable(object_)
            error_msg = (
                'Use + '
                + ref_value
                + '^'
                + str(len(object_.parameters))
                + ' instead of ['
                + ref_value
                + ', ...]'
            )
            identifier = object_.to_string()
            self.add_rule_status(container, Rule.FAILED, error_msg, identifier)

        return Rule.NA

    def get_expr_value(self, element) -> str:
        """Return the value of an expression."""
        if isinstance(element, suite.ExprId):
            reference = element.reference
            if isinstance(reference, suite.Constant):
                # resolve the constant: allow detecting [0, ZERO]
                return self.get_expr_value(element.reference.value)
        elif isinstance(element, suite.ConstValue):
            # remove _i16 etc.
            return element.value.split('_')[0]

        # default: return the string representation of the expression
        return element.to_string()


if __name__ == '__main__':
    # rule instantiated outside of a package
    InitializationOfArrays()
