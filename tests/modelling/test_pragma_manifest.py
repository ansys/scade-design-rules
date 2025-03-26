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

from ansys.scade.design_rules.modelling.pragma_manifest import PragmaManifest
from ansys.scade.design_rules.utils.rule import Rule
from tests.conftest import load_session

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.fixture(scope='session')
def session():
    """Unique instance of the test model PragmaManifest."""
    pathname = 'tests/modelling/PragmaManifest/PragmaManifest.etp'
    return load_session(pathname, project=pathname)


# instantiation alias
class TestPragmaManifest(PragmaManifest):
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
        ('P::AliasOk/', '', _OK),
        ('P::EnumNa/', '', _NA),
        ('P::EquivalentSubManifestOk/', '', _OK),
        ('P::ManifestNa/', '', _NA),
        ('P::ManifestOk/', '', _OK),
        ('P::NoManifestNa/', 'interface=true', _NA),
        ('P::NoManifestNa/', 'interface=false', _FAILED),
        ('P::NoManifestNok/', '', _FAILED),
        ('P::SubManifestOk/', '', _OK),
        ('P::SubNoManifestNok/', 'interface=true', _FAILED),
        # Lib not considered with the configuration KCG
        ('P::SubNoManifestNok/', 'configuration=KCG,interface=true', _NA),
        # Lib considered with a wrong configuration
        ('P::SubNoManifestNok/', 'configuration=Unknown,interface=true', _FAILED),
    ],
)
def test_pragma_manifest_nominal(session: suite.Session, path, param, expected):
    model = session.model

    type_ = model.get_object_from_path(path)
    assert type_
    rule = TestPragmaManifest(parameter=param)
    assert rule.on_start(model) == _OK
    status = rule.on_check(type_)
    assert status == expected


def test_pragma_manifest_robustness(session: suite.Session):
    model = session.model

    # parameter without value
    rule = TestPragmaManifest(parameter='configuration')
    assert rule.on_start(model) == _ERROR


@pytest.mark.parametrize(
    'path, expected',
    [
        ('S::Bool/', 'b'),
        ('S::Bool31/', 'b^31'),
        ('S::Char/', 'c'),
        ('S::Enum/', '(Enum)'),
        ('S::Float64/', 'f64'),
        ('S::Imported/', '(Imported)'),
        ('S::Int32/', 'i32'),
        ('S::Matrix/', 'b^31^9'),
        ('S::Point/', '(x:f32,y:f32)'),
        ('S::Signed8/', 'i8'),
        ('S::Signed9/', 'i9'),
        ('S::SignedN8/', 'i8'),
        ('S::SignedS8/', 'i8'),
        ('S::SignedX/', 'i(X)'),
        ('S::Speed/', 'f32'),
        ('S::Structure/', '(u:u16,s:f32,p:(x:f32,y:f32),m:b^31^9,i:(Imported))'),
        ('S::Uint16/', 'u16'),
        ('S::Undefined/', '()'),
        ('S::Unsigned16/', 'u16'),
    ],
)
def test_get_signature(session: suite.Session, path, expected):
    model = session.model

    type_ = model.get_object_from_path(path)
    assert type_
    rule = PragmaManifest()
    rule.on_start(model)
    status = rule.get_signature(type_)
    assert status == expected
