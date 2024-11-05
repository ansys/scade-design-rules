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

from ansys.scade.design_rules.utils.command import ParameterParser
from ansys.scade.design_rules.utils.rule import Rule

# shorter names
_OK = Rule.OK
_FAILED = Rule.FAILED
_ERROR = Rule.ERROR
_NA = Rule.NA


@pytest.mark.parametrize(
    'parameter, expected_value, expected_status',
    [
        ('', '', _ERROR),
        ('-t', '', _ERROR),
        ('--type', '', _ERROR),
        ('-x Ptr*', '', _ERROR),
        ('--type *Ptr', '*Ptr', _OK),
        ('-t Ptr*', 'Ptr*', _OK),
    ],
)
def test_command(parameter: str, expected_value: str, expected_status: int):
    parser = ParameterParser()
    parser.add_argument('-t', '--type', metavar='<type>', help='pointer type', required=True)
    options = parser.parse_command(parameter)
    message = parser.message
    if expected_status is _ERROR:
        assert options is None
        assert message
        print(message)
    else:
        assert options
        assert options.type == expected_value


def test_command_usage_default():
    parser = ParameterParser()
    parser.add_argument('-t', '--type', metavar='<type>', help='pointer type', required=True)
    print(parser.format_usage())
    assert parser.format_usage().startswith('usage: -')


def test_command_usage_prog():
    parser = ParameterParser(prog='test_prog')
    parser.add_argument('-t', '--type', metavar='<type>', help='pointer type', required=True)
    print(parser.format_usage())
    assert parser.format_usage().startswith('usage: test_prog -')
