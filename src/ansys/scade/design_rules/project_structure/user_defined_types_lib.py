# -*- coding: utf-8 -*-

# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Implements the UserDefinedTypesLib rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

import scade.model.suite as suite

from ansys.scade.apitools.query import get_type_name, is_array, is_structure
from ansys.scade.design_rules.utils.modelling import get_model
from ansys.scade.design_rules.utils.rule import SCK, Rule


class UserDefinedTypesLib(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0090',
        category='Project Structure',
        severity=Rule.REQUIRED,
        parameter='Domain',
        description=(
            'This rule checks if user-defined complex types used in top-level operators as '
            "interface are located in library projects prefixed with 'Lib' and the Domain name."
        ),
        label=(
            'Check that user-defined complex types used in operators '
            'at top-level are located in libraries'
        ),
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
            kinds=[SCK.INPUT, SCK.HIDDEN, SCK.OUTPUT],
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        if model.name.startswith('Lib'):
            self.set_message(
                'Provided model is located in a library project. '
                'This rule cannot check library projects!'
            )
            return Rule.ERROR

        return Rule.OK

    def on_check_ex(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        message = ''
        return_status = Rule.OK

        operator = object_.owner
        # Check if operator is at top-level: <model>/<package>::<operator>
        if not isinstance(operator.owner.owner, suite.Model):
            return Rule.NA

        model_name = operator.owner.owner.name
        type_ = object_.type
        if is_array(type_) or is_structure(type_):
            model = get_model(object_.type)
            assert model
            if model.name == model_name:
                message = (
                    get_type_name(type_) + ' is user-defined complex type at top-level. '
                    'Needs to be moved to a Library.'
                )
                return_status = Rule.FAILED
            elif model.name != 'Lib' + parameter:
                message = (
                    get_type_name(type_)
                    + ' is user-defined complex type which is not located in Lib'
                    + parameter
                    + ' project.'
                )
                return_status = Rule.FAILED

        self.set_message(message)
        return return_status


if __name__ == '__main__':
    # rule instantiated outside of a package
    UserDefinedTypesLib()
