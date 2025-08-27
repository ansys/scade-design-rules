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

"""Implements the CamelCaseNaming rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.naming import is_camel_case, is_scade_keyword
from ansys.scade.design_rules.utils.rule import SCK, Rule


class CamelCaseNaming(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0008',
        label='Camel case name',
        description=(
            'Each word composing a name shall start with an uppercase '
            'letter except the first one.\n'
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
                SCK.FIELD,
                SCK.SENSOR,
                SCK.INPUT,
                SCK.HIDDEN,
                SCK.OUTPUT,
                SCK.VARIABLE,
                SCK.SIGNAL,
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

    def on_check_ex(self, object_: suite.Object, parameter: str = '') -> int:
        """Return the evaluation status for the input object."""
        # since types and kinds can be overridden, make sure the object has a name
        try:
            name = object_.name.strip("'")
        except AttributeError:
            return Rule.NA

        # accept names suffixed by underscore when it is a keyword
        # TODO(Jean): allow the user to specify an additional list of keywords?
        # https://github.com/ansys/scade-design-rules/issues/29
        if name[-1] == '_' and is_scade_keyword(name[:-1]):
            name = name[:-1]
        if '_' in name:
            # captured by is_camel_case but provide a
            # more understandable message for a frequent mistake
            status = Rule.FAILED
            message = f"{name}: The name shall not contain '_'"
            self.set_message(message)
        elif not name[0].islower():
            # captured by is_camel_case but provide a
            # more understandable message for a frequent mistake
            status = Rule.FAILED
            message = f'{name}: The name shall start with a lowercase letter'
            self.set_message(message)
        elif not is_camel_case(name):
            status = Rule.FAILED
            message = f'{name}: The name shall be composed of a sequence of words'
            self.set_message(message)
        else:
            status = Rule.OK
        return status


if __name__ == '__main__':  # pragma: no cover
    CamelCaseNaming()
