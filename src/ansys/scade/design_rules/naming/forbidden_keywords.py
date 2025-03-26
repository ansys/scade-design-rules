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

"""Implements the ForbiddenKeywords rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


from pathlib import Path

import scade
import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class ForbiddenKeywords(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0022',
        category='Naming',
        severity=Rule.MANDATORY,
        types=None,
        parameter='keywords.txt',
        description=(
            'Specific keywords shall not be used as name.\n'
            '\n'
            'The parameter is a file containing the keywords, one word per line.'
        ),
        label='Forbidden Keyword',
    ):
        if not types:
            types = [
                suite.ConstVar,
                suite.Assertion,
                suite.NamedType,
                suite.Operator,
                suite.Diagram,
                suite.ControlBlock,
                suite.Package,
                suite.State,
                suite.Label,
                suite.CompositeElement,
            ]
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
        path = Path(model.descriptor.model_file_name).parent / parameter
        try:
            lines = path.open().read().split('\n')
        except BaseException as e:
            self.set_message(str(e))
            scade.output(str(e) + '\n')
            return Rule.ERROR

        self.keywords = {_ for _ in lines if _ and _[0] != '#'}
        return Rule.OK

    def on_check(self, object: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        # types can be redefined: protect against wrong input
        try:
            name = object.name
        except AttributeError:
            return Rule.NA

        if name in self.keywords:
            self.set_message('Forbidden keyword used as name')
            return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    ForbiddenKeywords()
