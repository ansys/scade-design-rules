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

"""Implements the NonLibProjects rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))

import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class NonLibProjects(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0059',
        category='Project Structure',
        severity=Rule.REQUIRED,
        parameter='Lib',
        description=(
            "This rule checks if all non-top-level operators, types, and constants of Non-'Lib' "
            'projects are located in other packages nested within the root package.'
        ),
        label=(
            'Projects shall contain only one top-level Operator and its used Types and Constants'
        ),
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.Package, suite.NamedType, suite.Constant],
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        if model.name.startswith(parameter):
            self.set_message(
                'Provided model is located in a library project. '
                'This rule cannot check library projects!'
            )
            self.model_is_library = True
        else:
            self.model_is_library = False

        return Rule.OK

    def on_check(self, object: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        if self.model_is_library:
            return Rule.OK

        if (
            isinstance(object, suite.Package)
            and isinstance(object.owner, suite.Model)
            and len(object.operators) > 1
        ):
            self.set_message('More than one top-level operator in project!')
            return Rule.FAILED

        if (
            isinstance(object, suite.Constant)
            and isinstance(object.owner, suite.Package)
            and isinstance(object.owner.owner, suite.Model)
        ):
            not_used_at_top_level = True
            if len(object.clients) == 0:
                not_used_at_top_level = False
            else:  # prevents unnecessary iteration when object.clients is empty
                for client in object.clients:
                    if (
                        isinstance(client.owner, suite.Package)
                        and isinstance(client.owner.owner, suite.Model)
                        and client.owner.owner.owner is None
                    ):
                        not_used_at_top_level = False
                        break

            if not_used_at_top_level:
                self.set_message('Constant defined at top-level package is not used at top-level!')
                return Rule.FAILED

        if (
            isinstance(object, suite.NamedType)
            and isinstance(object.owner, suite.Package)
            and isinstance(object.owner.owner, suite.Model)
        ):
            not_used_at_top_level = True
            if len(object.typed_objects) == 0:
                not_used_at_top_level = False
            else:  # prevents unnecessary iteration when object.typed_objects is empty
                for obj in object.typed_objects:
                    if (
                        isinstance(obj.owner, suite.Package)
                        and isinstance(obj.owner.owner, suite.Model)
                        and obj.owner.owner.owner is None
                    ):
                        not_used_at_top_level = False
                        break

            if not_used_at_top_level:
                self.set_message('Type defined at top-level package is not used at top-level!')
                return Rule.FAILED

        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    NonLibProjects()
