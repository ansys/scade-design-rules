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

"""Implements the HasLinkOrPartOfEquationSet rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))

import scade.model.suite as suite
import scade.model.traceability.local_trace_model as local_trace
import scade.model.traceability.traceability as trace

from ansys.scade.design_rules.utils.modelling import get_model
from ansys.scade.design_rules.utils.rule import SCK, Rule


class HasLinkOrPartOfEquationSet(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0026',
        category='Traceability',
        severity=Rule.REQUIRED,
        kinds=None,
        description=(
            'This rule checks if the elements have traceability links '
            'via the ALM Gateway or is part of an Equation Set.'
        ),
        label='Has traceability link',
    ):
        if not kinds:
            kinds = [SCK.CONSTANT, SCK.OPERATOR, SCK.DIAGRAM, SCK.EQ_SET]
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=False,
            default_param='',
            description=description,
            label=label,
            types=None,
            kinds=kinds,
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Load the traceability data."""
        # traceability dictionaries for each model/library
        self.almgr_dict = {}
        self.almgt_dict = {}
        for main_lib in model.all_libraries:
            path_name = main_lib.descriptor.model_file_name

            almgr_parser = trace.AlmgrParser()
            try:
                almgr_parser.parse(path_name)
                self.almgr_dict[main_lib] = almgr_parser
            except BaseException as e:
                self.set_message(f'almgr file could not be parsed ({e})')
                return Rule.ERROR

            almgt_parser = trace.AlmgtParser()
            try:
                almgt_parser.parse(path_name)
                self.almgt_dict[main_lib] = almgt_parser
            except BaseException as e:
                self.set_message(f'almgt file could not be parsed ({e})')
                return Rule.ERROR

        return Rule.OK

    def on_check_ex(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        # protect against kinds that are not applicable for this rule
        if not isinstance(object_, suite.Traceable):
            return Rule.NA

        if self._element_has_link(object_):
            has_link = True
        else:
            if isinstance(object_, suite.EquationSet):
                has_link = False
            else:
                has_link = self._is_part_of_equationset(object_)

        if not has_link:
            self.set_message('No linked requirement')
            return Rule.FAILED

        return Rule.OK

    def _element_has_link(self, element):
        model = get_model(element)
        # same check for libraries and main model
        almgr_parser = self.almgr_dict[model]
        almgt_parser = self.almgt_dict[model]

        number_of_links = 0
        # find links in almgr file
        for alm_document in almgr_parser.project.alm_documents:
            for requirement in alm_document.requirements:
                for incoming_link in requirement.incoming_links:
                    source = incoming_link.source
                    linked_object = model.get_object_from_oid(source.identifier)
                    if linked_object == element:
                        number_of_links += 1

        # update links with almgt information
        if almgt_parser.traceability:
            for link in almgt_parser.traceability.links:
                linked_object = model.get_object_from_oid(link.oid)
                if linked_object == element:
                    if link.action == local_trace.TraceType.ADD_LINK:
                        number_of_links += 1
                    elif link.action == local_trace.TraceType.UPDATE_LINK:
                        # TODO(Jean): needs to be checked
                        # https://github.com/ansys/scade-design-rules/issues/29
                        number_of_links += 1
                    elif link.action == local_trace.TraceType.REMOVE_LINK:
                        number_of_links -= 1

        return number_of_links > 0

    def _is_part_of_equationset(self, object_: suite.Object) -> bool:
        result = False
        if isinstance(object_, suite.Operator):
            for expr_call in object_.expr_calls:
                result |= self._has_equation_equation_set_with_req(expr_call.equation)
        elif (
            isinstance(object_, suite.LocalVariable) and (object_.is_input() or object_.is_hidden())
        ) or isinstance(object_, suite.Constant):
            for expr_id in object_.expr_ids:
                result |= self._has_equation_equation_set_with_req(expr_id.equation)
        elif isinstance(object_, suite.LocalVariable) and object_.is_output():
            for definition in object_.definitions:
                result |= self._has_equation_equation_set_with_req(definition)
        elif isinstance(object_, suite.LocalVariable):
            pass
        else:
            pass
        return result

    def _has_equation_equation_set_with_req(self, equation) -> bool:
        if equation is not None:
            for equation_set in equation.equation_sets:
                if self._element_has_link(equation_set):
                    return True
        return False


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    HasLinkOrPartOfEquationSet()
