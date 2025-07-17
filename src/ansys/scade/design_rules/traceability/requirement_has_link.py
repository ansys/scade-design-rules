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

"""Implements the RequirementHasLink rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))

import scade.model.suite as suite
import scade.model.traceability.local_trace_model as local_trace
import scade.model.traceability.traceability as trace

from ansys.scade.design_rules.utils.rule import Rule


class RequirementHasLink(Rule):
    """
    Implements the rule interface.

    This rule uses the 2023R1 requirement API
    """

    def __init__(
        self,
        id='id_0100',
        category='Traceability',
        severity=Rule.REQUIRED,
        parameter='withalmgt=true',
        description=(
            'This rule checks if all requirements in the requirement window are linked.\n'
            "parameter: 'withalmgt=' true or false: e.g.: withalmgt=true\n"
            'withalmgt=true: local links are taken into account.\n'
            'withalmgt=false: only pushed information is checked.'
        ),
        label='Requirement has traceability link',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.Model],
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = '') -> int:
        """Get the rule's parameters."""
        d = self.parse_values(parameter)
        if d is None:
            message = f"'{parameter}': parameter syntax error"
        else:
            withalmgt = d.get('withalmgt')
            if not withalmgt:
                message = f"'{parameter}': missing 'withalmgt' value"
            else:
                self.withalmgt = withalmgt == 'true'
                return Rule.OK

        self.set_message(message)
        return Rule.ERROR

    def on_check(self, object: suite.Object, parameter: str = '') -> int:
        """Return the evaluation status for the input object."""
        violated = False

        # check if object (model) is the main project and not a library model
        if object.library:
            return Rule.OK

        path = object.descriptor.model_file_name
        almgr_parser = trace.AlmgrParser()
        try:
            almgr_parser.parse(path)
        except Exception:
            return Rule.OK

        almgt_parser = trace.AlmgtParser()
        almgt_parser.parse(path)

        non_linked_reqs = []
        assert almgr_parser.project is not None  # nosec B101  # addresses linter
        for alm_document in almgr_parser.project.alm_documents:
            for requirement in alm_document.requirements:
                number_of_links = len(requirement.incoming_links)

                # update links_temp with almgt information
                if self.withalmgt and almgt_parser.traceability:
                    for link in almgt_parser.traceability.links:
                        if link.req_id == requirement.identifier:
                            if link.action == local_trace.TraceType.ADD_LINK:
                                number_of_links += 1
                            elif link.action == local_trace.TraceType.UPDATE_LINK:
                                # TODO(Jean): needs to be checked
                                # https://github.com/ansys/scade-design-rules/issues/29
                                number_of_links += 1
                            elif link.action == local_trace.TraceType.REMOVE_LINK:
                                number_of_links -= 1

                if number_of_links <= 0:
                    linked = False
                else:
                    linked = True

                if not linked:
                    non_linked_reqs.append(f'{alm_document.name}.{requirement.name}')
                    violated = True

        if violated:
            self.set_message(f'Not all Requirements have a link: {",".join(non_linked_reqs)}')
            return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    RequirementHasLink()
