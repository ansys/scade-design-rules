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

"""Implements the LibProjectsUsage rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class LibProjectsUsage(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0033',
        category='Project Structure',
        severity=Rule.REQUIRED,
        parameter='Lib',
        description=(
            'This rule checks if only library Projects (prefixed with Lib) are '
            'included in the current Project.'
        ),
        label="Only 'Lib' prefixed projects shall be used as library Projects",
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.Model],
            kinds=None,
        )

    def on_check(self, object: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        return_status = Rule.OK
        return_message = []
        for library in object.libraries:
            if not library.name.startswith(parameter):
                return_message.append('Included Project ' + library.name + ' is no Library project')
                return_status = Rule.FAILED

        if return_status == Rule.FAILED:
            return_message.append(
                "Library Projects shall contain the prefix '" + parameter + "' in their name!"
            )

        separator = '; '
        self.set_message(separator.join(return_message))
        return return_status


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    LibProjectsUsage()
