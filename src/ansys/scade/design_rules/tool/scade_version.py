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

"""Implements the ScadeVersion rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))


import re

import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class ScadeVersion(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0080',
        category='Tool',
        severity=Rule.REQUIRED,
        description=(
            'This rule checks if the version of the SCADE Suite models '
            'corresponds to a given version of SCADE.\n'
            "The parameter defines the version, for example '242' for SCADE Suite 2024 R2."
        ),
        label='Check the version of SCADE Suite models',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param='242',
            description=description,
            label=label,
            types=[suite.StorageUnit],
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        versions = [
            # 2019 R2
            (194, {'xmlns': 6, 'xmlns:ed': 6, 'xmlns:kcg': 3}),
            # 2020 R1
            (201, {'xmlns': 6, 'xmlns:ed': 7, 'xmlns:kcg': 3}),
            # 2022 R2
            (222, {'xmlns': 6, 'xmlns:ed': 8, 'xmlns:kcg': 3}),
        ]

        if not parameter.isdecimal():
            self.set_message(
                '%s: Incorrect version. The parameter must be an integer, for example: 242'
                % parameter
            )
            return Rule.ERROR
        version = int(parameter)
        if version < versions[0][0]:
            self.set_message('%s: Versions prior to 2019 R2 (194) are not supported.' % parameter)
            return Rule.ERROR

        # get the namespaces corresponding to the checked version
        for v in versions:
            if v[0] <= version:
                self.namespaces = v[1]
        return Rule.OK

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        path = object_.sao_file_name
        try:
            with open(path) as f:
                line = f.readline()
                if line.startswith('<?xml'):
                    line = f.readline()
                ns = re.findall(r'(xmlns[^=]*)="([^"]*)"', line)
                version = {_[0]: int(_[1].split('/')[-1]) for _ in ns}
        except (IOError, OSError):
            self.set_message('{0}: I/O Error'.format(path))
            return Rule.FAILED

        if version != self.namespaces:
            # report the first storage element contained in the file
            element = next((_ for _ in object_.elements if not isinstance(_, suite.Open)), None)
            if element:
                message = 'SCADE Version in xscade files does not match %s' % parameter
                self.add_rule_status(element, Rule.FAILED, message)
                return Rule.NA
            # otherwise, report the storage unit itself
            self.set_message('%s: SCADE Version does not match %s' % (path, parameter))
            return Rule.FAILED

        return Rule.OK


if __name__ == '__main__':
    # rule instantiated outside of a package
    ScadeVersion()
