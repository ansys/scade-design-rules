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

"""Implements the AnnNoteConnectedDataForPublicInterface rule."""

import scade
import scade.model.suite as suite

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


from ansys.scade.design_rules.utils.annotations import (
    get_first_note_by_type,
    get_note_type,
    is_ann_note_value_defined_and_get_value,
)
from ansys.scade.design_rules.utils.command import ParameterParser
from ansys.scade.design_rules.utils.modelling import is_visible
from ansys.scade.design_rules.utils.rule import SCK, Rule


class AnnNoteConnectedDataForPublicInterface(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0102',
        category='annotations',
        severity=Rule.REQUIRED,
        parameter='inport=RTB_i,outport=RTB_o',
        description=(
            "All interfaces used inside a public operator shall have the 'ConnectedData' "
            'annotation note.\n'
            'IsPrimary is set for outputs. ConnectorName = Input/Output_name + parameter'
        ),
        label='ConnectedData annotation note for interface',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            kinds=[SCK.INPUT, SCK.OUTPUT],
        )
        # note type as a feature for unit tests
        self.connected_data = 'ConnectedData'

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        # minimal level of backward compatibility
        parameter = (
            parameter.replace('inport=', '-i ').replace(',', ' ').replace('outport=', '-o ')
            if parameter
            else ''
        )
        print('parameter', parameter)
        self.note_type = get_note_type(model, self.connected_data)
        if not self.note_type:
            message = "'%s': unknown note type" % self.connected_data
        else:
            parser = ParameterParser(prog='')
            parser.add_argument(
                '-i', '--inport', help='Suffix for inputs', required=True, dest='in_port'
            )
            parser.add_argument(
                '-o', '--outport', help='Suffix for outputs', required=True, dest='out_port'
            )
            options = parser.parse_command(parameter)
            if not options:
                message = parser.message
            else:
                self.in_port = options.in_port
                self.out_port = options.out_port
                return Rule.OK

        self.set_message(message)
        scade.output(message + '\n')
        return Rule.ERROR

    def on_check_ex(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        if not is_visible(object_.owner):
            return Rule.NA

        self.violation_text_missing = []

        if object_.is_input():
            self._check_annotation(object_, self.in_port, False)
        else:
            assert object_.is_output()
            self._check_annotation(object_, self.out_port, True)

        if len(self.violation_text_missing) > 0:
            self.set_message('Annotation wrong: ' + ', '.join(self.violation_text_missing))
            return Rule.FAILED

        return Rule.OK

    def _check_annotation(self, object_: suite.Object, port: str, primary: bool):
        note = get_first_note_by_type(object_, self.note_type)
        defined, connected_port = is_ann_note_value_defined_and_get_value(note, 'ConnectedPort')
        if not defined:
            self.violation_text_missing.append('ConnectedPort not defined')
        else:
            if connected_port != port:
                self.violation_text_missing.append('ConnectedPort not ' + port)
        defined, connector_name = is_ann_note_value_defined_and_get_value(note, 'ConnectorName')
        if not defined:
            self.violation_text_missing.append('ConnectedName not defined')
        else:
            # note: if empty values are accepted for port, do not append '_' when empty
            expected_name = object_.name + '_' + port
            if connector_name != expected_name:
                self.violation_text_missing.append('ConnectorName not ' + expected_name)
        defined, is_primary = is_ann_note_value_defined_and_get_value(note, 'IsPrimary')
        if not defined:
            self.violation_text_missing.append('IsPrimary not defined')
        else:
            if is_primary != primary:
                self.violation_text_missing.append('IsPrimary not ' + str(primary))


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    AnnNoteConnectedDataForPublicInterface()
