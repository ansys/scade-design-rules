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

"""Implements the AnnNotesForBasicInterfaceTypes rule."""

import scade.model.suite as suite

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


from typing import List

from ansys.scade.apitools.query import get_cell_type, get_leaf_type, is_array
from ansys.scade.design_rules.utils.annotations import (
    AnnotationRule,
    ArgumentParser,
    get_first_note_by_type,
    is_ann_note_value_defined_and_get_value,
)
from ansys.scade.design_rules.utils.modelling import is_numeric, is_visible
from ansys.scade.design_rules.utils.rule import SCK, Rule


class AnnNotesForBasicInterfaceTypes(AnnotationRule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0099',
        category='annotations',
        severity=Rule.REQUIRED,
        parameter='-t SDD_TopLevel -v Public',
        description=(
            'All basic types used inside an operator interface shall have an annotation '
            'with the SI-Units, resolution, etc.\n'
            'NamedTypes are checked recursively.\n'
            "parameter: '-t': Name of the annotation note type, "
            "'--public ': Public interfaces only :e.g.: '-t SDD_TopLevel --public'"
        ),
        label='AnnotationNotes for basic types in operator interface',
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
            kinds=[SCK.INPUT, SCK.OUTPUT, SCK.HIDDEN],
        )
        self.std_fields = std_fields if std_fields else ['Description', 'Constraints']
        self.numeric_fields = (
            numeric_fields if numeric_fields else ['Min_Value', 'Max_Value', 'Unit_SI']
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        # minimal level of backward compatibility
        parameter = parameter.replace(',visibility=Public', ' --public')
        parameter = parameter.replace(',visibility=Private', '')

        result = super().on_start(model, parameter)
        if result == Rule.OK:
            assert self.options
            self.public = self.options.public
            # cache for checked named types of fields
            self.checked_typed = set()
        return result

    def add_arguments(self, parser: ArgumentParser):
        """Declare arguments in addition to the note type."""
        parser.add_argument('--public', help='Public interfaces only', action='store_true')

    def on_check_ex(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        # take care of sensors, should they be added later in the checked elements (kinds)
        declaration = object_.owner if isinstance(object_, suite.LocalVariable) else object_
        if not self.public or is_visible(declaration):
            self._check_object(object_)

        return Rule.NA

    def _check_object(self, typed: suite.TypedObject):
        # typed: context of the check, for annotations
        # must not be a table or a predefined type, that are typed objects without annotations
        assert not isinstance(typed, suite.Table)
        assert not isinstance(typed, suite.NamedType) or not typed.is_predefined()

        # use a cache to avoid duplicated analysis
        if typed in self.checked_typed:
            return
        self.checked_typed.add(typed)

        type_ = typed.type
        if is_array(type_):
            leaf = get_leaf_type(type_)
            # get the closest owner that is not a table: must be the leaf's owner
            typed = leaf.owner
            type_ = get_cell_type(leaf)

        if isinstance(type_, suite.NamedType) and type_.is_generic():
            # out of the rule's scope
            return
        elif isinstance(type_, suite.NamedType) and not type_.is_predefined():
            # bypass alias
            self._check_object(type_)
        elif isinstance(type_, suite.Structure):
            for element in type_.elements:
                # recurse
                self._check_object(element)
        else:
            # predefined, sized, imported, or enumeration types
            violation_text_missing = self._check_annotation(typed)
            if violation_text_missing:
                message = (
                    'Annotation missing for '
                    # TODO: object may not have a name
                    + typed.name
                    + ': '
                    + ', '.join(violation_text_missing)
                )
                self.add_rule_status(typed, Rule.FAILED, message, '')

    def _check_annotation(self, object_: suite.Annotable) -> List[str]:
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
    AnnNotesForBasicInterfaceTypes()
