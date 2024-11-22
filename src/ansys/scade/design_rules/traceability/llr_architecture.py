# -*- coding: utf-8 -*-

# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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

"""Implements the LLRArchitecture rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade
import scade.model.suite as suite

from ansys.scade.design_rules.utils.annotations import (
    AnnotationRule,
    ArgumentParser,
    get_first_note_by_type,
)
from ansys.scade.design_rules.utils.rule import Rule


class LLRArchitecture(AnnotationRule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0035',
        label="'Architecture' CE",
        description=(
            'Architecture Contributing Elements (CE) can be only equation sets or textual diagrams.'
        ),
        category='Traceability',
        severity=Rule.ADVISORY,
        parameter='-t DesignElement -a Nature -v Architecture',
        **kwargs,
    ):
        super().__init__(
            id=id,
            label=label,
            description=description,
            category=category,
            severity=severity,
            types=[suite.State, suite.Transition],
            has_parameter=True,
            default_param=parameter,
            **kwargs,
        )

        self.note_type = None
        self.note_attribute = None
        self.architecture = None

    def on_start(self, model: suite.Model, parameter: str) -> int:
        """Get the rule's parameters."""
        status = super().on_start(model, parameter)
        if status == Rule.OK:
            assert self.note_type
            assert self.options
            self.architecture = self.options.value
            for note_attribute in self.note_type.ann_att_definitions:
                if note_attribute.name == self.options.attribute:
                    self.note_attribute = note_attribute
                    break
            else:
                status = Rule.ERROR
                message = "'%s': unknown note attribute" % self.options.attribute
                self.set_message(message)
                scade.output(message + '\n')

        return status

    def add_arguments(self, parser: ArgumentParser):
        """Declare arguments in addition to the note type."""
        parser.add_argument(
            '-a', '--attribute', metavar='<attribute>', help='attribute name', required=True
        )
        parser.add_argument(
            '-v', '--value', metavar='<value>', help='value for architecture', required=True
        )

    def on_check(self, annotable: suite.Annotable, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        note = get_first_note_by_type(annotable, self.note_type)
        if note:
            for value in note.ann_att_values:
                if (
                    value.ann_att_definition == self.note_attribute
                    and value.to_string() == self.architecture
                ):
                    message = "The %s of the Contributing Element can't be '%s'" % (
                        self.note_attribute.name,
                        self.architecture,
                    )
                    self.set_message(message)
                    return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    LLRArchitecture()
