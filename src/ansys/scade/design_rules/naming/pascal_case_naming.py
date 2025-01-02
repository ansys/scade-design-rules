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

"""Implements the PascalCaseNaming rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.naming import is_pascal_case
from ansys.scade.design_rules.utils.rule import SCK, Rule


class PascalCaseNaming(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0078',
        label='Pascal case name',
        description=(
            'Each word composing a name shall start with an uppercase letter;\n'
            'The remainder of the word shall consist of lowercase letters and digits.'
        ),
        category='Naming',
        severity=Rule.REQUIRED,
        types=None,
        kinds=None,
        **kwargs,
    ):
        # default value for kinds when neither types nor kinds is specified
        if not types and not kinds:
            kinds = [
                SCK.TYPE,
                SCK.OPERATOR,
                SCK.DIAGRAM,
                SCK.STATE_MACHINE,
                SCK.STATE,
                SCK.IF_BLOCK,
                SCK.WHEN_BLOCK,
            ]
        super().__init__(
            id=id,
            label=label,
            description=description,
            category=category,
            severity=severity,
            types=types,
            kinds=kinds,
            has_parameter=False,
            **kwargs,
        )

    def on_check_ex(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        # since types and kinds can be overridden, make sure the object has a name
        try:
            name = object_.name.strip("'")
        except AttributeError:
            return Rule.NA

        if '_' in name:
            # captured by is_pascal_case but provide a
            # more understandable message for a frequent mistake
            status = Rule.FAILED
            message = "%s: The name shall not contain '_'" % name
            self.set_message(message)
        elif not name[0].isupper():
            # captured by is_pascal_case but provide a
            # more understandable message for a frequent mistake
            status = Rule.FAILED
            message = '%s: The name shall start with a capital letter' % name
            self.set_message(message)
        elif not is_pascal_case(name):
            status = Rule.FAILED
            message = '%s: The name shall be composed of a sequence of words' % name
            self.set_message(message)
        else:
            status = Rule.OK
        return status


if __name__ == '__main__':  # pragma: no cover
    PascalCaseNaming()
