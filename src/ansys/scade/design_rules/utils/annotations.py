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

"""Provides utilities for developing rules related to annotations."""

from typing import List, Optional, Tuple

import scade
import scade.model.suite.annotation as ann
import scade.model.suite.suite as suite

from ansys.scade.design_rules.utils.command import ArgumentParser, ParameterParser
from ansys.scade.design_rules.utils.rule import Rule


def get_note_type(model: suite.Model, name: str) -> Optional[ann.AnnNoteType]:
    """
    Get an annotation type by name, or ``None`` if not found.

    Parameters
    ----------
    model : suite.Model
        Input model.
    name : str
        Name of the note type to search.

    Returns
    -------
    ann.AnnNoteType
        Found note type, ``None`` otherwise.
    """
    return next((_ for _ in model.ann_note_types if _.name == name), None)


def get_notes_by_type(object_: suite.Annotable, type_: ann.AnnNoteType) -> List[ann.AnnNote]:
    """
    Get the annotation notes of an object by type.

    Parameters
    ----------
    object_ : suite.Annotable
        Input object.
    type_ : ann.AnnNoteType
        Type of the notes to search.

    Returns
    -------
    List[ann.AnnNote]
        Found notes.
    """
    return [_ for _ in object_.ann_notes if _.ann_note_type == type_]


def get_first_note_by_type(
    object_: suite.Annotable,
    type_: ann.AnnNoteType,
) -> Optional[ann.AnnNote]:
    """
    Get the first annotation note of an object by type.

    Parameters
    ----------
    object_ : suite.Annotable
        Input object.
    type_ : ann.AnnNoteType
        Type of the notes to search.

    Returns
    -------
    Optional[ann.AnnNote]
        Found note, otherwise ``None``.
    """
    notes = get_notes_by_type(object_, type_)
    return notes[0] if notes else None


def get_ann_note_by_name(object_: suite.Annotable, name: str) -> Optional[ann.AnnNote]:
    """
    Get the annotation note of an object by name, or ``None`` if not found.

    DEPRECATED: note names are not reliable, although it is unlikely

    Parameters
    ----------
    object_ : suite.Annotable
        Input object.
    name : str
        Name of the note to search.

    Returns
    -------
    Optional[ann.AnnNote]
        Found note, otherwise ``None``.
    """
    return next((_ for _ in object_.ann_notes if _.name == name), None)


def is_ann_note_value_defined_and_get_value(
    note: Optional[ann.AnnNote],
    element: str,
) -> Tuple[bool, str]:
    """
    Get the attribute value of a note and whether it is not empty.

    The attribute's value '-' is considered as empty.

    Parameters
    ----------
    note : Optional[ann.AnnNote]
        Input object.
    element : str
        Name of the attribute to retrieve.

    Returns
    -------
    Tuple[bool, str]
        ``(True, value)`` if the value exists and is not empty, otherwise ``(False, '')``.
    """
    att_value = note.get_ann_att_value_by_name(element) if note else None
    value = att_value.value if att_value else ''
    return value != '' and value != '-', value


class AnnotationRule(Rule):
    """Abstraction for rules that have a note type as parameter."""

    def on_start(self, model: suite.Model, parameter: str = '') -> int:
        """Get the note type parameter."""
        # backward compatibility
        parameter = parameter.replace('notetype=', '-t ') if parameter else ''
        parser = ParameterParser(prog='')
        parser.add_argument('-t', '--note_type', metavar='<type>', help='note type', required=True)
        self.add_arguments(parser)
        # parse the parameter and store the result for derived classes
        self.options = parser.parse_command(parameter)
        if self.options:
            # search for the note type
            self.note_type = get_note_type(model, self.options.note_type)
            if not self.note_type:
                message = f"'{self.options.note_type}': unknown note type"
            else:
                return Rule.OK
        else:
            message = parser.message

        self.set_message(message)
        # scade is a CPython module defined dynamically
        scade.output(message + '\n')  # type: ignore
        return Rule.ERROR

    def add_arguments(self, parser: ArgumentParser):
        """Declare arguments in addition to the note type."""
        pass
