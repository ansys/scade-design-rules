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

"""Implements the CommentHasSpecificHeadlines rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class CommentHasSpecificHeadlines(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0009',
        category='annotations',
        severity=Rule.REQUIRED,
        parameter='Purpose',
        label='The comment of an Operator shall have specific headlines.',
        types=None,
        description=(
            'The comment of an object shall have specific headlines defined in parameter.\n'
            'parameter: comma separated list of headlines, for example: Purpose, Algorithm'
        ),
    ):
        if not types:
            types = [suite.Operator]
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=types,
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        self.headlines = [_.strip() for _ in parameter.split(',')]
        return Rule.OK

    def on_check_ex(self, object: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        violation_no_text_found = False
        violation_not_all_headlines = False
        found_headlines = []
        messages = []

        number_of_headlines_found = 0
        for comment in object.comments:
            headline_found = False
            textline_found = False
            # is current line a headline
            for headline in self.headlines:
                if comment.startswith(headline):
                    headline_found = True
                    found_headlines.append(headline)
            # is current line a proper text
            if not headline_found:
                if not (comment.isspace() or comment == ''):
                    textline_found = True
            else:
                line = comment.lstrip(found_headlines[-1])
                if line.startswith(':'):
                    line = line.lstrip(':')
                if not (line.isspace() or line == ''):
                    textline_found = True

            if headline_found:
                number_of_headlines_found += 1
                if number_of_headlines_found >= 2:
                    violation_no_text_found = True
                    messages.append(f'No comment for {found_headlines[-2]}')
            if textline_found:
                number_of_headlines_found = 0

        if number_of_headlines_found >= 1:
            violation_no_text_found = True
            messages.append(f'No comment for {found_headlines[-1]}')

        if set(found_headlines) != set(self.headlines):
            violation_not_all_headlines = True
            messages.append('Not all headlines found.')

        if violation_no_text_found or violation_not_all_headlines:
            self.set_message('Comment not correct: ' + (',').join(messages))
            return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':
    # rule instantiated outside of a package
    CommentHasSpecificHeadlines()
