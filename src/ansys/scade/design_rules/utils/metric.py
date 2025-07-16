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
Provides a common base class for metrics, with additional services.

This class stubs the original ``Metric`` class for unit tests.
"""

from typing import List, Optional

import scade.model.suite as suite

try:
    # ignore F401: _register_metric made available for metrics, not used here
    # _register_metric is defined dynamically: ignore linter warning
    from scade.tool.suite import _register_metric  # noqa: F401  # type: ignore

    # _Metric defined hereafter is a stub, and thus can't match Metric
    from scade.tool.suite.metrics import Metric as _Metric  # type: ignore
except ImportError:

    class _Metric:
        """Stubs ``Metric`` for units tests."""

        def __init__(self, id: str, *args, **kwargs):
            self.id = id
            self.message = ''
            self.result = 0

        def set_message(self, message: str) -> None:
            """Store the message."""
            self.message = message

        def set_result_metric(self, result: int) -> None:
            """Stub the ``set_result_metric`` method."""
            self.result = result

        # Possible returned values by the following functions
        OK = 0
        FAILED = 1
        ERROR = 2
        # new 2023 R1, stands for NA
        NO_METRIC = 3


from .sck import SCK


class Metric(_Metric):
    """Base class for all metrics."""

    # set NA to OK until it is implemented
    # new 2023 R1: NA is there but named NO_RULE: let's keep NA
    try:
        NA = _Metric.NO_METRIC
    except BaseException:
        NA = 0

    def __init__(
        self,
        id: str,
        label: str,
        category: str,
        description: str,
        types: Optional[List[type]] = None,
        kinds: Optional[List[SCK]] = None,
        **kwargs,
    ):
        # discrimination of SCADE objects when the class isn't enough
        # compute the list of types when kinds is specified
        if kinds:
            types = [kind.value[0] for kind in kinds]
            self.kinds = kinds
        else:
            self.kinds = None
        # store the types, useful for unit tests
        self.types = types
        super().__init__(id, label, category, types, description=description, **kwargs)
        self.violations = {}

    def on_compute(self, object_: suite.Object) -> int:
        """Compute the metric for the input if it is compatible with the registered kinds."""
        if self.accept_kind(object_):
            return self.on_compute_ex(object_)
        else:
            return Metric.NA

    def on_compute_ex(self, object_: suite.Object) -> int:
        """Compute the metric for the input."""
        # must not be called if on_compute is redefined
        return Metric.ERROR

    def accept_kind(self, object_: suite.Object):
        """Return whether the input is compatible with the registered kinds."""
        if not self.kinds:
            return True

        for kind in self.kinds:
            type, filter = kind.value
            if isinstance(object_, type) and filter(object_):
                return True
        return False
