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

"""Implements the LLROnly rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

from typing import List

import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class LLROnly(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0037',
        label='Tracing elements must be CEs',
        description='The model elements tracing requirements shall be CEs.',
        category='Traceability',
        severity=Rule.ADVISORY,
        **kwargs,
    ):
        super().__init__(
            id=id,
            label=label,
            description=description,
            category=category,
            severity=severity,
            # suite.Traceable does not work, use suite.Object
            # types = [suite.Traceable],
            types=[suite.Object],
            has_parameter=False,
            **kwargs,
        )

    def on_check(self, traceable: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        if not isinstance(traceable, suite.Traceable):
            print('not traceable item', str(traceable))
            return Rule.NA

        ids = ', '.join(self.get_requirement_ids(traceable))
        if not self.is_llr(traceable) and ids:
            status = Rule.FAILED
            message = 'the element is not a CE: it shall not trace the requirement(s) %s' % ids
            self.set_message(message)
        else:
            status = Rule.OK
        return status

    def is_llr(self, traceable: suite.Traceable) -> bool:
        """
        Return whether the element is a contributing element for traceability.

        This method can be overridden in a derived class to consider different elements.
        """
        return type(traceable) in {
            suite.EquationSet,
            suite.State,
            suite.MainTransition,
            suite.ForkedTransition,
            suite.TextDiagram,
        }

    def get_requirement_ids(self, traceable: suite.Traceable) -> List[str]:  # pragma: no cover
        """
        Return the traced requirement IDs.

        This is a separate function to be redefined when ``Traceable.requirement_ids`` is
        not accessible (unit tests)
        """
        return traceable.requirement_ids


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    LLROnly()
