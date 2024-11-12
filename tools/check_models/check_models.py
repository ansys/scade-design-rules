# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 ANSYS, Inc. All rights reserved.
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

"""Checks there is at least one example per rule."""

from pathlib import Path
import sys


def check_models(root: Path) -> int:
    """Check there is one example per rule and vice versa."""
    exit_code = 0
    srcs = sorted(
        [
            _
            for _ in root.glob('src/ansys/scade/design_rules/*')
            if _.is_dir() and _.name != 'utils' and _.name != '__pycache__'
        ]
    )
    models = {_.name: _ for _ in root.glob('examples/*') if _.is_dir()}
    for src in srcs:
        try:
            model = models.pop(src.name)
        except KeyError:
            exit_code = 1
            print('%s: no examples' % src.name)
            continue
        examples = {_.name.lower(): _.name for _ in model.glob('*') if _.is_dir()}
        rules = sorted([_ for _ in src.glob('*.py') if _.name != '__init__.py'])
        for rule in rules:
            name = ''.join([_.capitalize() for _ in rule.stem.split('_')])
            try:
                examples.pop(name.lower())
            except KeyError:
                exit_code = 1
                print('%s/%s: no example' % (model.name, rule.name))
        for example in sorted(examples.keys()):
            # do not fail, some rules might have more than one example
            # exit_code = 1
            print('warning: %s/%s: no rule' % (model.name, examples[example]))
        # for example in sorted(list(examples)):
        #     failure = 1
        #     print('%s/%s: no rule' % (model.name, example))

    return exit_code


if __name__ == '__main__':
    # dir must be the root of the repository
    dir = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).parent.parent.parent
    sys.exit(check_models(dir))
