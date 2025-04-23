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

"""
Implements the CheckConfigurationCustom1 rule.

This rule has been developed specifically for a customer needs.
It may fulfill very specific purpose.
If you need to change this rule, consider forking/deriving to a new rule.
"""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import scade
import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class CheckConfigurationCustom1(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0104',
        category='configuration',
        severity=Rule.MANDATORY,
        parameter='conf=KCG,rootPackage=package1',
        description=(
            'Check given configuration for these settings:\n'
            "parameter: 'conf=' Name of configuration: e.g.: conf=KCG\n"
            "'rootPackage=' Name of root package: e.g.: rootPackage=package1"
        ),
        label='Check configuration',
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

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        d = self.parse_values(parameter)
        if d is None:
            message = f"'{parameter}': parameter syntax error"
        else:
            conf = d.get('conf')
            root_package = d.get('rootPackage')
            if not conf:
                message = f"'{parameter}': missing 'conf' value"
            elif not root_package:
                message = f"'{parameter}': missing 'rootPackage' value"
            else:
                self.conf = conf
                self.root_package = root_package
                return Rule.OK

        self.set_message(message)
        scade.output(message + '\n')
        return Rule.ERROR

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        failure_messages = []

        assert isinstance(object_, suite.Model)
        project = object_.project
        # check if object (model) is the main project and not a library model
        if not project:
            return Rule.OK

        configuration = project.find_configuration(self.conf)

        # 1 check for "no skip unused model objects"
        if project.get_bool_tool_prop_def('GENERATOR', 'SKIP_UNUSED', False, configuration):
            failure_messages.append('Skip unused model object is set')

        # 2 check for root operator setting
        rootnode_start = 'SoftwareComponents::ACD_Appl::'
        values = project.get_tool_prop_def('GENERATOR', 'ROOTNODE', [], configuration)
        for prop_value in values:
            if prop_value.startswith(rootnode_start):
                break
        else:
            failure_messages.append(f'Root node does not start with: {rootnode_start}')

        # 3 Code Integration settings
        if project.get_scalar_tool_prop_def('GENERATOR', 'TARGET_ADAPTOR', '', configuration):
            failure_messages.append('Code Integration Settings not correct')

        # 4 Optimization Settings
        if project.get_bool_tool_prop_def('GENERATOR', 'STATIC', False, configuration):
            failure_messages.append('Local variables as static is set')
        if project.get_bool_tool_prop_def('GENERATOR', 'INPUT_THRESHOLD', False, configuration):
            failure_messages.append('Input Threshold is set')

        # 5 Check User Config Setting
        user_config = '..\\..\\include\\' + object_.name + '_user_macros.h'
        value = project.get_scalar_tool_prop_def('GENERATOR', 'USER_CONFIG', '', configuration)
        if value != user_config:
            failure_messages.append(f'User Config not set to: {user_config}')

        # 6 Compiler settings
        value = project.get_scalar_tool_prop_def('SIMULATOR', 'CPU_TYPE', '', configuration)
        if value != 'win64':
            failure_messages.append('Simulator CPU type not correct')

        # 7 check annotation note MyAnnotationType_suite
        descriptor = object_.descriptor
        aty = (
            '..\\..\\..\\..\\architecture\\scade_plugins\\'
            'fcmsAnnotationType\\MyAnnotationType_suite.aty'
        )
        if aty not in descriptor.ann_type_files:
            failure_messages.append('MyAnnotationType_suite.aty not set properly')

        # 7 Prefix settings
        number_of_public = 0
        prefix_desired = ''
        root_package = None
        # assumption: top level package is "SoftwareComponents::ACD_Appl::"
        for package in object_.all_packages:
            if package.name == self.root_package:
                root_package = package
                break
        if root_package is not None:
            # assumption: only one public operator which is the root operator
            for operator in root_package.operators:
                if operator.visibility == 'Public':
                    number_of_public += 1
                    prefix_desired = (operator.name.split('_'))[-1]
        value = project.get_scalar_tool_prop_def('GENERATOR', 'GLOBALS_PREFIX', '', configuration)
        if value:
            if number_of_public == 1 and value != prefix_desired:
                failure_messages.append(f'Global Prefix not set to: {prefix_desired}')
        else:
            failure_messages.append('Global Prefix not set')

        if failure_messages:
            self.set_message(
                f'Configuration not correct ({len(failure_messages)}): '
                + ', '.join(failure_messages)
            )
            return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':
    # rule instantiated outside of a package
    CheckConfigurationCustom1()
