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

"""Implements the NoScadeLibrary rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


import os
from pathlib import Path

import scade
import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class NoScadeLibrary(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0061',
        label='SCADE libraries shall not be used in production',
        description=(
            'Only SCADE libraries that are under full control of the project'
            '(configuration management, verification) shall be used.\n'
            'In particular, the designer shall NOT use the SCADE product installation libraries, '
            'as they are delivered as examples.'
        ),
        category='Project Structure',
        severity=Rule.REQUIRED,
        parameter='upper_levels=1',
        **kwargs,
    ):
        super().__init__(
            id=id,
            label=label,
            description=description,
            category=category,
            severity=severity,
            types=[suite.Model],
            has_parameter=True,
            default_param=parameter,
            **kwargs,
        )
        self.upper_levels = 0

    def on_start(self, model: suite.Model, parameter: str) -> int:
        """Get the rule's parameters."""
        d = self.parse_values(parameter)
        if d is None:
            message = f"'{parameter}': parameter syntax error"
        else:
            upper_levels = d.get('upper_levels')
            self.upper_levels = int(upper_levels) if upper_levels is not None else 0
            return Rule.OK

        self.set_message(message)
        # scade is a CPython module defined dynamically
        scade.output(message + '\n')  # type: ignore
        return Rule.ERROR

    def on_check_ex(self, object_: suite.Object, parameter: str = '') -> int:
        """Return the evaluation status for the input object."""
        assert isinstance(object_, suite.Model)  # nosec B101  # addresses linter
        external_libraries = {}
        if object_.project:
            # $(SCADE) can be tested only for the main model's libraries
            for file in object_.project.file_refs:
                pathname = file.persist_as
                suffix = Path(pathname).suffix.lower()
                if suffix != '.etp' and suffix == '.vsp':
                    # not a library project
                    continue
                if '$(SCADE)' in pathname:
                    external_libraries[Path(file.pathname)] = pathname
                # TODO (Jean): this check can be optional
                # https://github.com/ansys/scade-design-rules/issues/29
                # elif (Path(pathname).is_absolute()):
                #     external_libraries.append(pathname)

        # make sure the dependencies are in sibling folders
        # or not absolute pathnames
        path_model = Path(object_.descriptor.model_file_name)
        for library in object_.libraries:
            path = Path(library.descriptor.model_file_name)
            try:
                rel_path = os.path.relpath(path, path_model.parent)
            except ValueError:  # More specific exception than BaseException
                external_libraries.setdefault(path, str(path))
                continue
            count = rel_path.count('..')
            if count > self.upper_levels and path not in external_libraries:
                external_libraries[path] = str(path)

        if external_libraries:
            status = Rule.FAILED
            message = (
                'The model {} shall not use SCADE product libraries or libraries outside '
                'of the CM workspace:\n{}'
            )
            self.set_message(message.format(object_.name, '\n'.join(external_libraries.values())))
        else:
            status = Rule.OK
        return status


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    NoScadeLibrary()
