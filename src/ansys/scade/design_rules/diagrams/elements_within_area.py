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

"""Implements the ElementsWithinArea rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))

import re

import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class ElementsWithinArea(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0015',
        description=('All elements shall be within the page format (A4, A3).'),
        label='Elements within area',
        category='Diagrams',
        parameter='margins=0; 0',
        severity=Rule.REQUIRED,
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[
                suite.Flow,
                suite.Transition,
            ],
            kinds=None,
        )
        # parameters
        self.x_margin = 0
        self.y_margin = 0
        # cache for boundaries
        self.cached_diagram = None
        self.cached_status = False
        # current format
        self.format = None
        # current left boundary
        self.min_x = 0
        # current upper boundary
        self.min_y = 0
        # current right boundary
        self.max_x = 0
        # current lower boundary
        self.max_y = 0
        # cache to report wrong formats only once
        self.wrong_formats = set()

        # formats available in the SCADE Editor, 1/100th of mm
        self.boundaries = {
            'A3': [29700, 42000],
            'A4': [21000, 29700],
            'B5': [18200, 25700],
            'LETTER': [21590, 27940],
            'LEGAL': [21590, 35560],
        }

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Reset the caches and parse the parameters."""
        self.wrong_formats = set()

        # default message if syntax error
        message = f"'{parameter}': syntax error, expected 'margins= <value>; <value>'"
        parameter = 'margins= 0; 0' if parameter is None else parameter
        d = self.parse_values(parameter)
        if d:
            margins = d.get('margins')
            try:
                self.x_margin, self.y_margin = (int(_) for _ in margins.split(';'))
                return Rule.OK
            except BaseException:
                pass

        self.set_message(message)
        return Rule.ERROR

    def on_check(self, object_: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        pe = object_.presentation_element
        if not pe or not isinstance(pe.diagram, suite.NetDiagram):
            return Rule.NA

        diagram = pe.diagram
        status = self.set_boundaries(diagram)
        if not status:
            if diagram not in self.wrong_formats:
                # cache the diagram and not the format to report
                # the error once per diagram
                self.wrong_formats.add(diagram)
                self.set_message(f'Format {self.format} not supported')
                return Rule.FAILED
            else:
                return Rule.NA

        items = set()
        if isinstance(pe, suite.Box):
            status = not self.is_box_outside_area(pe.position, pe.size)
            if isinstance(pe, suite.EquationGE):
                if not status:
                    items.add('equation')
                # check outgoing edges
                for edge in pe.out_edges:
                    if self.is_link_outside_area(edge.points):
                        # do not use logical shortcut to report all findings
                        status = False
                        items.add(f'edge {edge.left_var.name}')
        else:
            assert isinstance(pe, suite.TransitionGE)
            if self.is_box_outside_area(pe.label_pos, pe.label_size):
                status = False
                items.add('label')
            if self.is_link_outside_area(pe.points):
                status = False
                items.add('link')

        if not status:
            message = 'Element outside area'
            if items:
                message += ' ({})'.format(', '.join(sorted(items)))

            self.set_message(message)
            return Rule.FAILED

        return Rule.OK

    def set_boundaries(self, diagram: suite.NetDiagram) -> bool:
        """Cache the boundaries and margins for the input diagram."""
        if diagram == self.cached_diagram:
            return self.cached_status
        self.cached_diagram = diagram
        self.format = diagram.format.split()[0]
        if self.format not in self.boundaries.keys():
            # custom format
            regexp = r'(.*)\s*\(\s*(\d+)\s+(\d+)\s*\)\s*'
            match = re.match(regexp, diagram.format)
            if match:
                groups = match.groups()
                self.format = groups[0]
                self.boundaries[self.format] = [int(_) * 100 for _ in groups[1:]]
            else:
                self.cached_status = False
                return False

        if diagram.landscape:
            self.max_x = self.boundaries[self.format][1] - self.y_margin
            self.max_y = self.boundaries[self.format][0] - self.x_margin
        else:
            self.max_x = self.boundaries[self.format][0] - self.x_margin
            self.max_y = self.boundaries[self.format][1] - self.y_margin

        self.cached_status = True
        return True

    def is_box_outside_area(self, pos, size) -> bool:
        """Return whether an box is within the area."""
        x, y = pos
        w, h = size
        return x < self.min_x or y < self.min_y or x + w > self.max_x or y + h > self.max_y

    def is_link_outside_area(self, points) -> bool:
        """Return whether a line is within the area."""
        for x, y in points:
            if x < self.min_x or y < self.min_y or x > self.max_x or y > self.max_y:
                return True
        return False


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    ElementsWithinArea()
