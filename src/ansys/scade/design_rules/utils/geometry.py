# -*- coding: utf-8 -*-

# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Utilities for intersection checks."""


class Point:
    """Point."""

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rect2D:
    """Rectangle."""

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2


class Line2D:
    """Segment."""

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def online(self, line, p: Point) -> bool:
        """Return whether p is on the line."""
        if (
            (p.x <= max(line.p1.x, line.p2.x))
            and (p.x >= min(line.p1.x, line.p2.x))
            and (p.y <= max(line.p1.y, line.p2.y))
            and (p.y >= min(line.p1.y, line.p2.y))
        ):
            return True
        return False

    def direction(self, a: Point, b: Point, c: Point) -> int:
        """Return the direction of an angle."""
        val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
        # colinear
        if val == 0:
            return 0
        # anti-clockwise direction
        elif val < 0:
            return 2
        # clockwise direction
        else:
            return 1

    def is_intersect_line(self, line) -> bool:
        """Return whether the line intersects another line."""
        # four direction for two lines and points of line line
        dir1 = self.direction(self.p1, self.p2, line.p1)
        dir2 = self.direction(self.p1, self.p2, line.p2)
        dir3 = self.direction(line.p1, line.p2, self.p1)
        dir4 = self.direction(line.p1, line.p2, self.p2)

        # lines are intersecting
        if dir1 != dir2 and dir3 != dir4:
            return True
        # when p2 of line2 are on the line1
        if dir1 == 0 and self.online(self, line.p1):
            return True
        # when p1 of line2 are on the line1
        if dir2 == 0 and self.online(self, line.p2):
            return True
        # when p2 of line1 are on the line2
        if dir3 == 0 and self.online(line, self.p1):
            return True
        # when p1 of line1 are on the line2
        if dir4 == 0 and self.online(line, self.p2):
            return True

        return False

    def is_intersection_rect(self, rect: Rect2D) -> bool:
        """Return whether the line intersects a rectangle."""
        rect_point1 = Point(rect.p1.x, rect.p2.y)
        rect_point2 = Point(rect.p2.x, rect.p1.y)
        line1 = Line2D(rect.p1, rect_point1)
        line2 = Line2D(rect.p1, rect_point2)
        line3 = Line2D(rect_point1, rect.p2)
        line4 = Line2D(rect_point2, rect.p2)

        res = (
            self.is_intersect_line(line1)
            or self.is_intersect_line(line2)
            or self.is_intersect_line(line3)
            or self.is_intersect_line(line4)
        )
        if res:
            return True

        return False
