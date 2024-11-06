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

"""Implements the LLRNature rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.annotations import AnnotationRule, get_first_note_by_type
from ansys.scade.design_rules.utils.rule import Rule


class LLRNature(AnnotationRule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0036',
        label='CE must have a design annotation',
        description=(
            "The contributing elements shall have an annotation 'DesignElement' "
            "with a property 'Nature'.\n"
            "Parameter: '-t': Name of the note type: e.g.: '-t DesignElement'"
        ),
        category='Traceability',
        severity=Rule.ADVISORY,
        types=None,
        parameter='-t DesignElement',
        **kwargs,
    ):
        if not types:
            types = [suite.EquationSet, suite.TextDiagram, suite.State, suite.Transition]
        super().__init__(
            id=id,
            label=label,
            description=description,
            category=category,
            severity=severity,
            types=types,
            has_parameter=True,
            default_param=parameter,
            **kwargs,
        )

        self.note_type = None

    def on_start(self, model: suite.Model, parameter: str) -> int:
        """Get the rule's parameters."""
        # backward compatibility
        parameter = parameter.replace('note=', '-t ') if parameter else ''
        return super().on_start(model, parameter)

    def on_check(self, annotable: suite.Annotable, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        note = get_first_note_by_type(annotable, self.note_type)
        if note:
            status = Rule.OK
        else:
            status = Rule.FAILED
            message = 'the Contributing Element shall have an annotation %s' % self.note_type.name
            self.set_message(message)
        return status


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    LLRNature()
