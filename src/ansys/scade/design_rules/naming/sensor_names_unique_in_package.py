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

"""Implements the SensorNamesUniqueInPackage rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class SensorNamesUniqueInPackage(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0121',
        category='Naming',
        severity=Rule.REQUIRED,
        description='The name of a Sensor shall not be used for variables in the same package.',
        label='The name of a Sensor shall not be used for variables in the same package.',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=False,
            default_param='',
            description=description,
            label=label,
            types=[suite.LocalVariable],
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Cache all sensors."""
        self.sensors = {_.name: _ for _ in model.all_sensors}
        return Rule.OK

    def on_check(self, object: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        violated = False

        if object.is_internal():
            # no need to check
            return Rule.NA

        sensor = self.sensors.get(object.name)
        if sensor:
            # raise a violation if the variable is defined in the sensor's package
            # or sub-packages
            owner = object.owner
            while owner:
                if owner == sensor.owner:
                    violated = True
                    break
                owner = owner.owner

        if violated:
            self.set_message('Variable name is also used for the sensor: ' + sensor.get_full_path())
            return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':
    # rule instantiated outside of a package
    SensorNamesUniqueInPackage()
