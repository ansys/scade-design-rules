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

"""Implements the NameStructureDiagram rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import re

import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import SCK, Rule


class NameStructureDiagram(Rule):
    """Implements the rule interface."""

    pattern_multiple = re.compile(r'(.*[^0-9])\d+')

    def __init__(
        self,
        id='id_0047',
        label='Diagram name',
        description=(
            'When there are several diagrams in a scope, '
            'the name of each diagram shall be characteristic of its function.\n'
            'Otherwise the default name created by the editor shall be '
            'updated to the name of its scope.'
        ),
        category='Naming',
        severity=Rule.ADVISORY,
        **kwargs,
    ):
        super().__init__(
            id=id,
            label=label,
            description=description,
            category=category,
            severity=severity,
            kinds=[SCK.DIAGRAM],
            has_parameter=False,
            **kwargs,
        )

    def on_check_ex(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        name = object_.name
        scope = object_.owner
        scope_name = '' if isinstance(scope, suite.Action) else scope.name
        if len(scope.diagrams) == 1:
            if not scope_name:
                # TODO: one may want top compare the name with the one
                #       we get from get_full_path
                status = Rule.NA
            elif name != scope.name:
                # TODO: As an alternative, make sure the name of the scope is
                #       included in the name of the diagram
                message = f'{name}: The name shall be the name of its scope {scope.name}'
                self.set_message(message)
                status = Rule.FAILED
            else:
                status = Rule.OK
        else:
            # fail when the name differ from a sibling by a suffix number
            # or that has the same name as the scope
            pattern_scope = re.compile(scope_name + r'_?\d+')
            if pattern_scope.fullmatch(name):
                # check of diagram name vs owner name
                message = f"{name}: The name derives from its scope's name instead of a description"
                self.set_message(message)
                status = Rule.FAILED
            else:
                match = self.pattern_multiple.fullmatch(name)
                if match:
                    # check for a similar sibling name => copies
                    prefix = match.group(1)
                    pattern_prefix = re.compile(prefix + r'\d+')
                    for diagram in scope.diagrams:
                        if diagram != object_ and pattern_prefix.fullmatch(diagram.name):
                            message = f'{name}: The name shall be a description'
                            self.set_message(message)
                            status = Rule.FAILED
                            break
                    else:
                        status = Rule.OK
                else:
                    status = Rule.OK
        return status


if __name__ == '__main__':  # pragma: no cover
    NameStructureDiagram()
