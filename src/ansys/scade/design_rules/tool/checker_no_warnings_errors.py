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

"""Implements the CheckerNoWarningsErrors rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))

import scade.model.suite as suite

from ansys.scade.apitools.info.install import get_scade_home
from ansys.scade.design_rules.utils.rule import SCK, Rule


class CheckerNoWarningsErrors(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0118',
        category='Tool',
        severity=Rule.REQUIRED,
        parameter='conf=KCG',
        description=(
            'This rule checks if the semantic checker reports no errors and no warnings.\n'
            'parameter: conf=configuration name'
        ),
        label='Semantic checker shall raise no errors and warnings',
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
            kinds=[SCK.MODEL],
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        d = self.parse_values(parameter)
        if d is None:
            d = f"'{parameter}': parameter syntax error"
        else:
            configuration = d.get('conf')
            if not configuration:
                message = f"'{parameter}': missing 'conf' value"
            else:
                self.configuration = configuration
                return Rule.OK

        self.set_message(message)
        return Rule.ERROR

    def on_check_ex(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        violated = False

        # check if object (model) is the main project and not a library model
        if object_.library:
            return Rule.NA

        # create command line call
        scade_home = str(get_scade_home())
        scade_path = scade_home + r'\SCADE\bin\scade.exe'
        pathname = object_.descriptor.model_file_name
        call = f'"{scade_path}" -check "{pathname}" -conf {self.configuration}'

        # execute call
        import os

        stream = os.popen(call)
        output = stream.read()
        outputs = output.split('\n')

        # parse result string for errors and warnings
        import re

        x = re.search(r'^Checker ends with (\d) error.*(\d) warning', outputs[0])
        errors = x.groups()[0]
        warnings = x.groups()[1]

        if int(errors) > 0 or int(warnings) > 0:
            violated = True

        if violated:
            self.set_message(outputs[0])
            return Rule.FAILED

        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    CheckerNoWarningsErrors()
