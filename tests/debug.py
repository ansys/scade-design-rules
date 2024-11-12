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

"""Script for debugging rules."""

import argparse

# this needs to be included before compute_metrics and check_rules
from ansys.scade.apitools import declare_project  # noqa: F401

# isort: split

from scade.model.suite import get_roots as get_sessions
from scade.tool.suite.metrics import compute_metrics
from scade.tool.suite.rules import check_rules


def main(args):
    """Invoke the internal SCADE Checker on the input project."""
    assert declare_project
    declare_project(args.project)
    if args.action == 'metrics':
        compute_metrics(get_sessions()[0], args.configuration)
    elif args.action == 'rules':
        check_rules(get_sessions()[0], args.configuration)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Debug environment for Rules and Metrics development.'
    )
    parser.add_argument('project', help='Scade Project file')
    parser.add_argument(
        '-c', '--configuration', metavar='<configuration>', help='configuration', required=True
    )
    parser.add_argument('-a', '--action', choices=['metrics', 'rules'], required=True)

    main(parser.parse_args())

"""
Command line examples:

tests/naming/Names/Names.etp -c MetricRule -a rules
"""
