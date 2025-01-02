# -*- coding: utf-8 -*-

# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

from ansys.scade.design_rules.modelling.no_anonymous_type import NoAnonymousType
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def session():
    """Unique instance of the test model NoAnonymousType."""
    pathname = 'tests/modelling/NoAnonymousType/NoAnonymousType.etp'
    return load_session(pathname, project=pathname)


# instantiation alias
class TestNoAnonymousType(NoAnonymousType):
    __test__ = False

    def __init__(self, parameter=None, **kwargs):
        self.parameter = parameter
        super().__init__(id='', parameter=self.parameter, **kwargs)

    def on_start(self, model=None, parameter=None):
        parameter = parameter if parameter else self.parameter
        return super().on_start(model=model, parameter=parameter)

    def on_check(self, object, parameter=None):
        parameter = parameter if parameter else self.parameter
        return super().on_check(object, parameter=parameter)


@pytest.mark.parametrize(
    'path, param, expected',
    [
        # default parameters
        ('P::Root/ok/', '', _OK),
        ('P::Root/nokStruct/', '', _FAILED),
        ('P::Root/nokNull/', '', _FAILED),
        ('P::Root/okDefined/', '', _OK),
        ('P::Root/nokArray/', '', _FAILED),
        ('P::Root/nokTable/', '', _FAILED),
        ('P::Size/na/', '', _NA),
        ('P::Size/naNull/', '', _NA),
        ('P::Size/naArray/', '', _NA),
        ('P::Polymorphic/na/', '', _NA),
        ('P::Polymorphic/naNull/', '', _NA),
        ('P::Polymorphic/naT/', '', _NA),
        ('P::Call/na/', '', _NA),
        ('P::Call/naNull/', '', _NA),
        ('P::Call/naArray/', '', _NA),
        ('P::Lib/ok/', '', _OK),
        ('P::Lib/nokNull/', '', _FAILED),
        ('P::Lib/nokArray/', '', _FAILED),
        ('P::Imported/ok/', '', _OK),
        ('P::Imported/nokNull/', '', _FAILED),
        ('P::Imported/nokArray/', '', _FAILED),
        # Lib not considered with the configuration KCG
        ('P::Root/ok/', 'configuration=KCG', _OK),
        ('P::Root/nokNull/', 'configuration=KCG', _FAILED),
        ('P::Root/nokArray/', 'configuration=KCG', _FAILED),
        ('P::Lib/ok/', 'configuration=KCG', _NA),
        ('P::Lib/nokNull/', 'configuration=KCG', _NA),
        ('P::Lib/nokArray/', 'configuration=KCG', _NA),
        # Lib considered with a wrong configuration
        ('P::Lib/ok/', 'configuration=Unkwnon', _OK),
        ('P::Lib/nokNull/', 'configuration=Unkwnon', _FAILED),
        ('P::Lib/nokArray/', 'configuration=Unkwnon', _FAILED),
    ],
)
def test_no_anonymous_type_nominal(session: suite.Session, path, param, expected):
    model = session.model

    variable = model.get_object_from_path(path)
    assert variable
    rule = TestNoAnonymousType(parameter=param)
    assert rule.on_start(model) == _OK
    status = rule.on_check(variable)
    assert status == expected


def test_no_anonymous_type_robustness(session: suite.Session):
    model = session.model

    # parameter without value
    rule = TestNoAnonymousType(parameter='configuration')
    assert rule.on_start(model) == _ERROR
