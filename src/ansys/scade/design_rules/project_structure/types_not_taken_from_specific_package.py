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

"""Implements the TypesNotTakenFromSpecificPackage rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.modelling import is_visible
from ansys.scade.design_rules.utils.rule import SCK, Rule


class TypesNotTakenFromSpecificPackage(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0086',
        category='Modelling',
        severity=Rule.REQUIRED,
        parameter='Obsolete,TobeAligned',
        description=(
            'Interface data types from public operators shall not be taken from given packages.\n'
            "parameter: list of packages separated by comma: e.g.: 'Obsolete,TobeAligned'"
        ),
        label='Types not from specific packages',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=None,
            kinds=[SCK.INPUT, SCK.HIDDEN, SCK.OUTPUT, SCK.SENSOR],
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        self.forbidden_packages = []
        names = {_.strip() for _ in parameter.split(',')}
        self.forbidden_packages = {_ for _ in model.all_packages if _.name in names}
        return Rule.OK

    def on_check_ex(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        # if not sensor, verify the owning operator is public
        if isinstance(object_.owner, suite.Operator) and not is_visible(object_.owner):
            return Rule.NA

        type_ = object_.type
        if type_.owner in self.forbidden_packages:
            self.set_message('Type is taken from forbidden package: ' + type_.get_full_path())
            return Rule.FAILED

        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    TypesNotTakenFromSpecificPackage()
