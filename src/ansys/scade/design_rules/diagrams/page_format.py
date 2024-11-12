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

"""Implements the PageFormat rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class PageFormat(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0113',
        category='Diagrams',
        severity=Rule.REQUIRED,
        parameter='format=A4,orientation=Landscape',
        label='Check Page Format.',
        types=None,
        description=(
            'This rule checks if the page format is set properly.\n'
            'param1: format=A3 A4 B5 etc.\n'
            'param2: orientation=Portrait Landscape\n'
            'For example: format=A3,orientation=Landscape'
        ),
    ):
        if not types:
            types = [suite.NetDiagram]
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
        d = self.parse_values(parameter)
        if d is None:
            d = "'%s': parameter syntax error" % parameter
        else:
            format = d.get('format')
            orientation = d.get('orientation')
            if format is None:
                message = "'%s': missing 'format' value" % parameter
            elif orientation is None:
                message = "'%s': missing 'orientation' value" % parameter
            else:
                self.format = format
                self.orientation = orientation
                return Rule.OK

        self.set_message(message)
        return Rule.ERROR

    def on_check(self, object: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        violated = False
        failure_messages = []

        net_diagram = object

        if not net_diagram.format.startswith(self.format):
            violated = True
            failure_messages.append('Format is set to ' + net_diagram.format)

        if net_diagram.landscape and self.orientation != 'Landscape':
            violated = True
            failure_messages.append('Orientation is set to Landscape.')
        if not net_diagram.landscape and self.orientation != 'Portrait':
            violated = True
            failure_messages.append('Orientation is set to Portrait.')

        if violated:
            self.set_message(','.join(failure_messages))
            return Rule.FAILED

        return Rule.OK


if __name__ == '__main__':
    # rule instantiated outside of a package
    PageFormat()
