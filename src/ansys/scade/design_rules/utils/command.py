# -*- coding: utf-8 -*-

# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Provides a command line parser for the rules' parameter."""

from argparse import ArgumentParser, Namespace
import shlex
from typing import Optional


class ParameterParser(ArgumentParser):
    """
    Override the exit and error functions to not exit the application.

    Add a method a parse a parameter string.
    """

    def __init__(self, **kwargs):
        # remove the prefix for usage unless specified
        if 'prog' not in kwargs:
            kwargs = kwargs.copy()
            kwargs['prog'] = ''
        super().__init__(**kwargs)

    def error(self, message: str):
        """
        Override ``error`` to store the message instead of exiting.

        Parameters
        ----------
        message : str
            Error message.
        """
        self.messages.append(message)

    def print_help(self):
        """Override ``print_help`` to store the message instead of raising an exception."""
        self.messages.append(self.format_help())

    def exit(self):
        """Override ``exit`` to not exit the application."""
        pass

    def parse_command(self, command: str) -> Optional[Namespace]:
        """
        Parse a parameter using ArgumentParser.

        Returns None if an error is raised, and the messages are
        accessible in the attribute ``messages``.

        Parameters
        ----------
        command : str
            Input command line.

        Returns
        -------
        Optional[Namespace]
            Result of the parsing or None if an exception is raised.
        """
        # side_effect with self.error
        self.messages = []
        args = shlex.split(command, posix=False)
        ns = super().parse_args(args)
        return ns if not self.messages else None

    @property
    def message(self) -> str:
        """Return a text with all the messages."""
        return '\n'.join(self.messages)

    def format_usage(self) -> str:
        """Return the parser's usage without ``[h]`` and trailing empty line."""
        return super().format_usage().strip('\n').replace(' [-h]', '')
