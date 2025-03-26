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


import pytest
import scade.model.suite as suite

from ansys.scade.design_rules.naming.name_structure_diagram import NameStructureDiagram
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session
from tests.naming.utils import NamedVisitor

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def session() -> suite.Session:
    # unique model for these tests
    session = load_session('tests/naming/Diagrams/Diagrams.etp')
    return session


@pytest.mark.parametrize(
    'test_case',
    [
        ('Diagrams::Failure::', _FAILED),
        ('Diagrams::Success::', _OK),
    ],
)
def test_name_struct_diagram(session: suite.Session, test_case):
    # make sure all the named model elements are valid or not, depending
    # the owning package
    path, expected = test_case
    model = session.model

    package = model.get_object_from_path(path)
    assert isinstance(package, suite.Package)
    visitor = NamedVisitor('test_name_struct_diagrams', NameStructureDiagram, expected)
    visitor.visit(package)
    assert not visitor.error
