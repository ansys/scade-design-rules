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

"""Implements the NoFloats rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import scade.model.suite as suite

from ansys.scade.apitools.query import get_leaf_type, is_predefined
from ansys.scade.design_rules.utils.rule import Rule


class NoFloats(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0056',
        category='Modelling',
        severity=Rule.MANDATORY,
        description='Floats shall NOT be used',
        label='No floats',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=False,
            default_param='',
            description=description,
            label=label,
            types=[suite.NamedType, suite.ExprType, suite.ConstVar, suite.ConstValue],
            kinds=None,
        )

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        if isinstance(object_, suite.ConstVar):
            is_float = self._is_float_in_type(object_.type)
        elif isinstance(object_, suite.NamedType):
            is_float = self._is_float_in_type(object_)
        elif isinstance(object_, suite.ExprType):
            is_float = self._is_float_in_type(object_.type)
        elif isinstance(object_, suite.ConstValue):
            is_float = object_.kind == 'Float'
        else:
            is_float = False

        if is_float:
            self.set_message('Float found')
            return Rule.FAILED

        return Rule.OK

    def _is_float_in_type(self, type_: suite.Type) -> bool:
        """Return whether the type depends on float.

        :param predef_type:
        :return:
        """
        leaf = get_leaf_type(type_)
        if is_predefined(leaf) and (leaf.name == 'float32' or leaf.name == 'float64'):
            return True
        elif isinstance(leaf, suite.Table):
            return self._is_float_in_type(leaf.type)
        elif isinstance(leaf, suite.Structure):
            for element in leaf.elements:
                if self._is_float_in_type(element.type):
                    return True
        return False


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    NoFloats()
