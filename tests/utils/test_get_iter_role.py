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


import pytest
import scade.model.suite as suite

from ansys.scade.design_rules.utils.modelling import IR, get_iter_role

# SC_ECK_* codes
from ansys.scade.design_rules.utils.predef import (
    SC_ECK_FOLD as _FOLD,
    SC_ECK_FOLDI as _FOLDI,
    SC_ECK_FOLDW as _FOLDW,
    SC_ECK_FOLDWI as _FOLDWI,
    SC_ECK_MAP as _MAP,
    SC_ECK_MAPFOLD as _MAPFOLD,
    SC_ECK_MAPFOLDI as _MAPFOLDI,
    SC_ECK_MAPFOLDW as _MAPFOLDW,
    SC_ECK_MAPFOLDWI as _MAPFOLDWI,
    SC_ECK_MAPI as _MAPI,
    SC_ECK_MAPW as _MAPW,
    SC_ECK_MAPWI as _MAPWI,
)
from tests.conftest import load_session

# shorter names
_NONE = IR.NONE
_INDEX = IR.INDEX
_ACC_IN = IR.ACC_IN
_ACC_OUT = IR.ACC_OUT
_CONTINUE = IR.CONTINUE


@pytest.fixture(scope='session')
def session() -> suite.Session:
    # unique model for these tests
    session = load_session('tests/utils/GetIterRole/GetIterRole.etp')
    return session


@pytest.mark.parametrize(
    'test_case',
    [
        (_MAP, [_NONE, _NONE, _NONE, _NONE, _NONE, _NONE, _NONE, _NONE]),
        (_MAPI, [_INDEX, _NONE, _NONE, _NONE, _NONE, _NONE, _NONE, _NONE]),
        (_MAPW, [_NONE, _NONE, _NONE, _NONE, _CONTINUE, _NONE, _NONE, _NONE]),
        (_MAPWI, [_INDEX, _NONE, _NONE, _NONE, _CONTINUE, _NONE, _NONE, _NONE]),
        (_FOLD, [_ACC_IN, _NONE, _NONE, _NONE, _ACC_OUT, _NONE, _NONE, _NONE]),
        (_FOLDI, [_INDEX, _ACC_IN, _NONE, _NONE, _ACC_OUT, _NONE, _NONE, _NONE]),
        (_FOLDW, [_ACC_IN, _NONE, _NONE, _NONE, _CONTINUE, _ACC_OUT, _NONE, _NONE]),
        (_FOLDWI, [_INDEX, _ACC_IN, _NONE, _NONE, _CONTINUE, _ACC_OUT, _NONE, _NONE]),
        (_MAPFOLD, [_ACC_IN, _ACC_IN, _ACC_IN, _NONE, _ACC_OUT, _ACC_OUT, _ACC_OUT, _NONE]),
        (_MAPFOLDI, [_INDEX, _ACC_IN, _ACC_IN, _ACC_IN, _ACC_OUT, _ACC_OUT, _ACC_OUT, _NONE]),
        (_MAPFOLDW, [_ACC_IN, _ACC_IN, _ACC_IN, _NONE, _CONTINUE, _ACC_OUT, _ACC_OUT, _ACC_OUT]),
        (_MAPFOLDWI, [_INDEX, _ACC_IN, _ACC_IN, _ACC_IN, _CONTINUE, _ACC_OUT, _ACC_OUT, _ACC_OUT]),
    ],
)
def test_get_iter_role(session: suite.Session, test_case):
    code, roles = test_case
    model = session.model

    operator = model.get_object_from_path('P::Operator/')
    assert operator
    call = next((_ for _ in operator.expr_calls if int(_.inst_name) == code))
    assert call
    assert call.modifier is not None
    modifier = call.modifier
    modifier.predef_opr = code
    for variable, role in zip(operator.inputs + operator.hiddens + operator.outputs, roles):
        assert get_iter_role(variable, call) == role
