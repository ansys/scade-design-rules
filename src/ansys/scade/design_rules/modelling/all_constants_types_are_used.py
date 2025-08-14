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

"""Implements the AllConstantsTypesAreUsed rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))

import scade
import scade.model.suite as suite

from ansys.scade.design_rules.utils.annotations import (
    AnnotationRule,
    get_first_note_by_type,
    is_ann_note_value_defined_and_get_value,
)
from ansys.scade.design_rules.utils.rule import Rule


class AllConstantsTypesAreUsed(AnnotationRule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0002',
        category='Modelling',
        severity=Rule.REQUIRED,
        parameter='-t ConstantUsage',
        label='All constants and types are used at least once',
        types=None,
        description=(
            'All constants and types are used at least once.\nFor constants, it is also checked '
            "if the annotation note 'only external use' is set.\n"
            'parameter:\n'
            "* '-t': Name of the annotation note type\n"
        ),
    ):
        if not types:
            types = [suite.Constant, suite.NamedType]
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

    def on_check(self, object: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        violated = False

        if isinstance(object, suite.NamedType):
            if not object.typed_objects:
                violated = True
        elif isinstance(object, suite.Constant):
            if not object.expr_ids:
                # check for annotation note for external use mark
                ann_note = get_first_note_by_type(object, self.note_type)
                defined, value = is_ann_note_value_defined_and_get_value(
                    ann_note, 'isExternallyUsed_TrueFalse'
                )
                violated = not defined or not value
        else:
            scade.output(f'Rule not implemented for {object.__class__.__name__}')
            Rule.ERROR

        if violated:
            self.set_message(f'{object.__class__.__name__} {object.name} not used in model.')
            return Rule.FAILED

        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    AllConstantsTypesAreUsed()
