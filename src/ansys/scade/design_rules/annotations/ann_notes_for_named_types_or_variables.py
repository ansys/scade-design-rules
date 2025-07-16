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

"""Implements the AnnNotesForNamedTypesOrVariables rule."""

import scade.model.suite as suite

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


from typing import List

from ansys.scade.apitools.query import get_cell_type
from ansys.scade.design_rules.utils.annotations import (
    AnnotationRule,
    get_first_note_by_type,
    is_ann_note_value_defined_and_get_value,
)
from ansys.scade.design_rules.utils.modelling import is_numeric
from ansys.scade.design_rules.utils.rule import SCK, Rule


class AnnNotesForNamedTypesOrVariables(AnnotationRule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0006',
        category='annotations',
        severity=Rule.REQUIRED,
        parameter='-t SDD_TopLevel',
        description=(
            'If a variable has a NumericType then the numeric type shall have an annotation '
            'with the SI-Units, resolution, etc.\n'
            'If the variable has a basic type the variable itself shall have the annotation.\n'
            'If both are defined then raise a warning.\n'
            "parameter: '-t': Name of the annotation note type: e.g.: '-t SDD_TopLevel'"
        ),
        label='AnnotationNotes for variables with basic type',
        # ease customization
        std_fields=None,
        numeric_fields=None,
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
            kinds=[SCK.TYPE, SCK.INPUT, SCK.HIDDEN, SCK.OUTPUT],
        )
        self.std_fields = std_fields if std_fields else ['Description', 'Constraints']
        self.numeric_fields = (
            numeric_fields if numeric_fields else ['Min_Value', 'Max_Value', 'Unit_SI']
        )

    def on_check_ex(self, object_: suite.Object, parameter: str = '') -> int:
        """Return the evaluation status for the input object."""
        violation_text_missing = []

        # the registered objects are typed
        assert isinstance(object_, suite.TypedObject)
        if self._is_eligible_for_annotation(object_):
            # named type or local variable
            violation_text_missing = self._check_annotation(object_)
        else:
            # search for an aliased type eligible for annotation
            type_ = object_.type
            # loop on aliases and tables
            while isinstance(type_, suite.TypedObject):
                if self._is_eligible_for_annotation(type_):
                    ann_note = get_first_note_by_type(object_, self.note_type)
                    if ann_note:
                        # redundant because predefined type aliases are expected
                        # to have an annotation, cf. check above
                        violation_text_missing = ['Redundant annotation note found.']
                    break
                else:
                    type_ = type_.type

        if violation_text_missing:
            self.set_message(
                f'Annotation missing for {object_.name}: {", ".join(violation_text_missing)}'
            )
            return Rule.FAILED

        return Rule.OK

    def _is_eligible_for_annotation(self, typed: suite.TypedObject) -> bool:
        """Check if the given object is eligible for annotation."""
        # named types are both types and typed objects
        if isinstance(typed, suite.NamedType) and (typed.is_imported() or typed.is_generic()):
            # type itself, if it has a constraint, i.e. is numeric,
            # else nothing can be said about the nature of the type
            return typed.constraint is not None
        type_ = typed.type
        if isinstance(type_, suite.Table):
            type_ = get_cell_type(type_)
        return (
            type_.is_predefined()
            or isinstance(type_, suite.Enumeration)
            or isinstance(type_, suite.SizedType)
        )

    def _check_annotation(self, object_: suite.Object) -> List[str]:
        """Check the annotation for the given object."""
        violation_text_missing = []

        ann_note = get_first_note_by_type(object_, self.note_type)
        for field in self.std_fields:
            defined, _ = is_ann_note_value_defined_and_get_value(ann_note, field)
            if not defined:
                violation_text_missing.append(field)
        if is_numeric(object_.type) or (
            isinstance(object_, suite.NamedType) and is_numeric(object_)
        ):
            for field in self.numeric_fields:
                defined, _ = is_ann_note_value_defined_and_get_value(ann_note, field)
                if not defined:
                    violation_text_missing.append(field)

        return violation_text_missing


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    AnnNotesForNamedTypesOrVariables()
