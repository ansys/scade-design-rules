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

"""Implements the LevelOfPackages metric."""

if __name__ == '__main__':  # pragma: no cover
    # metric instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

import scade.model.suite as suite

from ansys.scade.design_rules.utils.metric import SCK, Metric


class LevelOfPackages(Metric):
    """Implements the metric interface."""

    def __init__(
        self,
        id='id_0127',
        category='Counters',
        label='Number of package levels',
        description='Number of package levels.',
    ):
        super().__init__(
            id=id,
            label=label,
            category=category,
            description=description,
            types=None,
            kinds=[SCK.PACKAGE],
        )

    def on_compute_ex(self, package: suite.Package) -> int:
        """Compute the metric for the input object."""
        result = self._max_level(package)
        self.set_result_metric(result)

        return Metric.OK

    def _max_level(self, package: suite.Package) -> int:
        level = max((self._max_level(_) for _ in package.packages)) if package.packages else 0
        return level + 1


if __name__ == '__main__':  # pragma: no cover
    # metric instantiated outside of a package
    LevelOfPackages()
