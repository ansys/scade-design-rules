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

"""Implements the NameLengthOfElement rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class NameLengthOfElement(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0041',
        category='Naming',
        severity=Rule.REQUIRED,
        parameter='32',
        types=None,
        description="Detect elements with a name length of more than 'parameter-value'",
        label='Name length too long',
    ):
        if not types:
            types = [suite.Package]
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=types,
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        if not parameter.strip().isdecimal():
            self.set_message(
                'Parameter for rule is not an integer or lower than zero: ' + parameter
            )
            return Rule.ERROR
        self.max_length = int(parameter)

        return Rule.OK

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        try:
            name = object_.name
        except AttributeError:
            # the list of registered types is open
            # -> ignore anonymous objects
            # alternative: filter the list of type in __init__
            return Rule.NA

        if len(name) > self.max_length:
            if isinstance(object_, suite.LocalVariable):
                if object_.is_input():
                    element = 'Input'
                elif object_.is_output():
                    element = 'Output'
                elif object_.is_hidden():
                    element = 'Hidden Input'
                elif object_.is_local():
                    if object_.probe:
                        element = 'Probe'
                    else:
                        element = 'Local Variable'
                else:
                    element = 'Variable'
            else:
                element = object_.__class__.__name__

            self.set_message(element + ' name longer than ' + parameter + ' characters')
            return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':
    # rule instantiated outside of a package
    NameLengthOfElement()
