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


import scade
import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class LLRNature(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0036',
        label='CE must have a design annotation',
        description=(
            "The contributing elements shall have an annotation 'DesignElement'"
            " with a property 'Nature'"
        ),
        category='Traceability',
        severity=Rule.ADVISORY,
        types=None,
        parameter='note=DesignElement',
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
        assert model is not None

        d = self.parse_values(parameter)
        if d is None:
            message = "'%s': parameter syntax error" % parameter
        else:
            note_type_name = d.get('note')
            if note_type_name is None:
                message = "'%s': missing 'note' value" % parameter
            else:
                for note_type in model.ann_note_types:
                    if note_type.name == note_type_name:
                        self.note_type = note_type
                        return Rule.OK
                else:
                    message = "'%s': unknown note type" % parameter

        self.set_message(message)
        scade.output(message + '\n')
        return Rule.ERROR

    def on_check(self, annotable: suite.Annotable, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        for note in annotable.ann_notes:
            if note.ann_note_type == self.note_type:
                status = Rule.OK
                break
        else:
            status = Rule.FAILED
            message = 'the Contributing Element shall have an annotation %s' % self.note_type.name
            self.set_message(message)
        return status


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    LLRNature()
