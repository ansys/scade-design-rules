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

"""Implements the IdenticalForProducerConsumer rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


from typing import Set

import scade.model.suite as suite

from ansys.scade.design_rules.utils.annotations import (
    AnnotationRule,
    get_first_note_by_type,
    is_ann_note_value_defined_and_get_value,
)
from ansys.scade.design_rules.utils.rule import SCK, Rule


class IdenticalForProducerConsumer(AnnotationRule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0027',
        category='annotations',
        severity=Rule.REQUIRED,
        parameter='-t SDD_TopLevel',
        description=(
            'The annotation notes for producer and consumer shall be identical '
            'if they both exist.\n'
            "If only the consumer has a note raise a 'redefine' warning.\n\n"
            'parameter:\n'
            "* '-t': Name of the annotation note type"
        ),
        label='Identical annotations for producer and consumer',
        # ease customization
        min_field='Min_Value',
        max_field='Max_Value',
        unit_field='Unit_SI',
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
        self.min_field = min_field
        self.max_field = max_field
        self.unit_field = unit_field

    def on_check_ex(self, object: suite.Object, parameter: str = '') -> int:
        """Return the evaluation status for the input object."""
        self.violated = False
        self.violation_text = []

        consumer = object
        producers = set()

        if consumer.is_output():
            producers.update(self._get_producers(consumer))
        else:
            # assert consumer.is_input() or consumer.is_hidden()
            # get operator in which the inputs and hiddens are defined
            operator = consumer.operator
            # create a combined list of all inputs and hiddens.
            # This is possible since in the IDE the hiddens always come at the end
            all_inputs = operator.inputs + operator.hiddens
            # get position of input/hidden in operator interface
            input_pos_in_operator = all_inputs.index(consumer)
            # go through all occurrences where the operator is called from another operator
            for expr_call in operator.expr_calls:
                parameters = expr_call.parameters
                if len(all_inputs) - 1 == len(parameters):
                    if input_pos_in_operator == 0:
                        # it is the index of a 'i' iterator: no dependencies
                        continue
                    input_pos_in_operator -= 1
                else:
                    if len(all_inputs) != len(parameters):  # pragma: no cover
                        # incorrect model
                        continue
                param = parameters[input_pos_in_operator]
                if isinstance(param, suite.ExprId) and isinstance(
                    param.reference, suite.LocalVariable
                ):
                    producers.update(self._get_producers(param.reference))

        for producer in producers:
            self._compare_annotation_notes(producer, consumer)

        if self.violated:
            self.set_message(f'Annotation notes issues: {";".join(self.violation_text)}')
            return Rule.FAILED
        return Rule.OK

    def _get_producers(self, consumer: suite.LocalVariable) -> Set[suite.LocalVariable]:
        """Return the producers of the consumer."""
        producers = set()
        # analyze the equations in which the consumer is produced
        for prev_eq in consumer.definitions:
            right = prev_eq.right
            if isinstance(right, suite.ExprId) and isinstance(right.reference, suite.LocalVariable):
                producer = right.reference
                if producer.is_input():
                    producers.add(producer)
                else:
                    # recurse
                    producers.update(self._get_producers(producer))
            elif isinstance(right, suite.ExprCall):
                # right side is a called operator: could be inside iterator
                if right.operator:
                    # get operator which is called and find connected output.
                    called_op = right.operator
                    # get position of local variable in left side if equation.
                    local_var_pos_in_lefts = prev_eq.lefts.index(consumer)
                    if len(called_op.outputs) < len(prev_eq.lefts):
                        if local_var_pos_in_lefts == 0:
                            # exit index: no dependencies
                            continue
                        else:
                            local_var_pos_in_lefts -= 1
                    if local_var_pos_in_lefts >= len(called_op.outputs):  # pragma: no cover
                        # incorrect model
                        continue
                    producer = called_op.outputs[local_var_pos_in_lefts]
                    producers.add(producer)
                # else: predefined operator: stop the analysis
        return producers

    def _compare_annotation_notes(
        self, producer: suite.LocalVariable, consumer: suite.LocalVariable
    ):
        """Compare the annotation notes of producer and consumer."""
        self.violated = False

        ann_note_consumer = get_first_note_by_type(consumer, self.note_type)
        ann_note_producer = get_first_note_by_type(producer, self.note_type)

        # Unit SI check
        if self.unit_field:
            consumer_unit_si_defined, consumer_unit_si = is_ann_note_value_defined_and_get_value(
                ann_note_consumer, self.unit_field
            )
            producer_unit_si_defined, producer_unit_si = is_ann_note_value_defined_and_get_value(
                ann_note_producer, self.unit_field
            )
            if consumer_unit_si_defined:
                if not producer_unit_si_defined:
                    self.violated = True
                    self.violation_text.append(f'{self.unit_field}: {producer.name} is redefined.')
                elif consumer_unit_si != producer_unit_si:
                    self.violated = True
                    self.violation_text.append(
                        f'{self.unit_field}: {consumer.name} != {producer.name}.'
                    )

        # Range check min
        if self.min_field:
            consumer_min_defined, consumer_min = is_ann_note_value_defined_and_get_value(
                ann_note_consumer, self.min_field
            )
            producer_min_defined, producer_min = is_ann_note_value_defined_and_get_value(
                ann_note_producer, self.min_field
            )
            if consumer_min_defined:
                if not producer_min_defined:
                    self.violated = True
                    self.violation_text.append(f'{self.min_field}: {producer.name} is redefined.')
                elif float(consumer_min) > float(producer_min):
                    self.violated = True
                    self.violation_text.append(
                        f'{self.min_field}: {consumer.name} > {producer.name}.'
                    )

        # Range check max
        if self.max_field:
            consumer_max_defined, consumer_max = is_ann_note_value_defined_and_get_value(
                ann_note_consumer, self.max_field
            )
            producer_max_defined, producer_max = is_ann_note_value_defined_and_get_value(
                ann_note_producer, self.max_field
            )
            if consumer_max_defined:
                if not producer_max_defined:
                    self.violated = True
                    self.violation_text.append(f'{self.max_field}: {producer.name} is redefined.')
                elif float(consumer_max) < float(producer_max):
                    self.violated = True
                    self.violation_text.append(
                        f'{self.max_field}: {consumer.name} < {producer.name}.'
                    )


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    IdenticalForProducerConsumer()
