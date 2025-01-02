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

import scade.model.suite as suite
from scade.model.suite.visitors import Visit

from ansys.scade.design_rules.utils.modelling import get_full_path_ex
from ansys.scade.design_rules.utils.rule import Rule

# overwrite Rule.NA so that tests cases can differentiate OK/NA
if Rule.NA == Rule.OK:
    Rule.NA = 3


# note: check the traces once when the algorithm is changed
class NamedVisitor(Visit):
    def __init__(self, context: str, rule: type, expected):
        self.context = context
        self.rule = rule
        self.expected = expected
        self.error = False

    def visit_object(self, object_: suite.Object, *args):
        super().visit_object(object_, *args)
        try:
            _ = object_.name
        except BaseException:
            return

        rule = self.rule()
        if not rule.kinds and type(object_) not in rule.types:
            print(
                '%s: skipping %s (%s)' % (self.context, get_full_path_ex(object_), object_._class_)
            )
            return
        status = rule.on_check(object_)
        if status == Rule.NA:
            print(
                '%s: not applicable %s (%s)'
                % (self.context, get_full_path_ex(object_), object_._class_)
            )
        else:
            # print('%s: %s (%s)' % (self.context, get_full_path_ex(object_), object_._class_))
            if status != self.expected:
                print('rule fails for', get_full_path_ex(object_))
                self.error = True
