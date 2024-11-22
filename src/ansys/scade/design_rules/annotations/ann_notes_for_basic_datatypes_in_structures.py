# -*- coding: utf-8 -*-

# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
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

"""Implements the AnnNotesForBasicDataTypesInStructures rule."""

from typing import List

import scade.model.suite as suite

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


from ansys.scade.apitools.query import get_cell_type, get_leaf_type, is_array
from ansys.scade.design_rules.utils.annotations import (
    AnnotationRule,
    get_first_note_by_type,
    is_ann_note_value_defined_and_get_value,
)
from ansys.scade.design_rules.utils.modelling import is_numeric
from ansys.scade.design_rules.utils.rule import Rule


class AnnNotesForBasicDataTypesInStructures(AnnotationRule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0005',
        category='annotations',
        severity=Rule.REQUIRED,
        parameter='-t SDD_TopLevel',
        description=(
            'Sub-element of structure definitions for component I/O and TPCs that has basic '
            'datatypes shall be described with below information in its notes field\n'
            '* Description:\n* Constraints:\n\n'
            'If not Booleans\n* Min_Value:\n* Max_Value:\n* Unit(SI):\n\n'
            "parameter: '-t': Name of the annotation note type: e.g.: '-t SDD_TopLevel'"
        ),
        label='AnnotationNotes for basic data types in structures',
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
            types=[suite.CompositeElement],
            kinds=None,
        )
        self.std_fields = std_fields if std_fields else ['Description', 'Constraints']
        self.numeric_fields = (
            numeric_fields if numeric_fields else ['Min_Value', 'Max_Value', 'Unit_SI']
        )

    def on_check_ex(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        if not isinstance(object_.owner.owner, suite.NamedType):
            # field of an anonymous structure: ignore
            return Rule.NA

        if is_array(object_.type):
            type_ = get_cell_type(object_.type, True)
        else:
            type_ = object_.type
        type_ = get_leaf_type(type_)
        if isinstance(type_, suite.Structure):
            if not isinstance(type_.owner, suite.NamedType):
                # anonymous structure that can't be evaluated
                self.set_message('Anonymous structures not supported: ' + object_.name)
                return Rule.FAILED
            else:
                return Rule.NA

        violation_text_missing = self._check_annotation(object_, type_)

        if violation_text_missing:
            self.set_message(
                'Annotation missing for ' + object_.name + ': ' + ', '.join(violation_text_missing)
            )
            return Rule.FAILED
        return Rule.OK

    def _check_annotation(self, object_: suite.CompositeElement, type_: suite.Type) -> List[str]:
        violation_text_missing = []

        ann_note = get_first_note_by_type(object_, self.note_type)
        for field in self.std_fields:
            defined, _ = is_ann_note_value_defined_and_get_value(ann_note, field)
            if not defined:
                violation_text_missing.append(field)
        if is_numeric(type_):
            for field in self.numeric_fields:
                defined, _ = is_ann_note_value_defined_and_get_value(ann_note, field)
                if not defined:
                    violation_text_missing.append(field)

        return violation_text_missing


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    AnnNotesForBasicDataTypesInStructures()
