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

"""Implements the LineCrossing rule."""

if __name__ == '__main__':
    # rule instantiated outside of a package
    from os.path import abspath, dirname
    import sys

    sys.path.append(abspath(dirname(dirname(dirname(dirname(dirname(__file__)))))))

import pathlib

import scade.model.suite as suite

from ansys.scade.design_rules.utils.geometry import Line2D, Point, Rect2D
from ansys.scade.design_rules.utils.rule import Rule


class GElement:
    """Abstraction for a graphical element to ease the verifications."""

    def __init__(self, x, y, width, height, name_of_edge, element_type, target):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name_of_element = name_of_edge
        self.element_type = element_type
        self.target = target


def line_crosses_element(start_line_x, start_line_y, end_line_x, end_line_y, g_element) -> bool:
    """Return whether a line crosses an element."""
    res1 = False
    if isinstance(g_element.target, suite.Edge):
        line1 = Line2D(
            Point(g_element.x, g_element.y),
            Point(g_element.x + g_element.width, g_element.y + g_element.height),
        )
        line2 = Line2D(Point(start_line_x, start_line_y), Point(end_line_x, end_line_y))
        res1 = line1.is_intersect_line(line2)
    else:
        rect = Rect2D(
            Point(g_element.x, g_element.y),
            Point(g_element.x + g_element.width, g_element.y + g_element.height),
        )
        line = Line2D(Point(start_line_x, start_line_y), Point(end_line_x, end_line_y))
        res1 = line.is_intersection_rect(rect)
    return res1


def is_point_inside_area(point_x, point_y, x, y, width, height) -> bool:
    """Return whether a point is within an area."""
    return (
        (point_x >= x) and (point_y >= y) and (point_x <= (x + width)) and (point_y <= (y + height))
    )


class LineCrossing(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0034',
        category='Readability',
        parameter='lines=yes',
        label='LineCrossing',
        severity=Rule.REQUIRED,
        description=(
            'Overlapping of edges with edges or other elements shall be prevented.\n'
            'Element overlapping is prevented by SCADE editor.\n'
            'Setting the parameter to lines=no will no longer report edges crossing edges.'
        ),
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.NetDiagram],
            kinds=None,
        )

        # list of already found elements. new elements are checked against this list
        self.g_elements = []
        # buffer for found overlapping within own diagram.
        self.found_elements = []
        self._project_name = ''

    def on_start(self, model: suite.Model, parameter: str = None) -> int:
        """Get the rule's parameters."""
        project_path = model.project.pathname.replace('\\', '/')
        self._project_name = str(pathlib.Path(project_path).name)

        d = self.parse_values(parameter)
        if d is None:
            message = "'%s': parameter syntax error" % parameter
        else:
            check_lines = d.get('lines')
            if check_lines is None:
                message = "'%s': missing 'lines' value" % parameter
            else:
                self.check_lines = check_lines.lower() == 'yes'
                return Rule.OK

        self.set_message(message)
        return Rule.ERROR

    def on_check(self, object: suite.Object, parameter: str = None) -> int:
        """Return the evaluation status for the input object."""
        # list of already found elements. new elements are checked against this list
        self.g_elements = []
        # buffer for found overlapping within own diagram.
        self.found_elements = []

        # first add all box elements to gElements list
        for diagram_object in object.presentation_elements:
            if (
                isinstance(diagram_object, suite.StateMachineGE)
                or isinstance(diagram_object, suite.StateGE)
                or isinstance(diagram_object, suite.IfBlockGE)
                or isinstance(diagram_object, suite.WhenBlockGE)
            ):
                self.add_element(
                    diagram_object.position[0],
                    diagram_object.position[1],
                    diagram_object.size[0],
                    diagram_object.size[1],
                    diagram_object.presentable.name,
                    None,
                    diagram_object.presentable,
                )
            if isinstance(diagram_object, suite.TransitionGE):
                self.add_element(
                    diagram_object.label_pos[0],
                    diagram_object.label_pos[1],
                    diagram_object.label_size[0],
                    diagram_object.label_size[1],
                    'Transition',
                    None,
                    diagram_object.presentable,
                )
            if isinstance(diagram_object, suite.ActionGE):
                self.add_element(
                    diagram_object.position[0],
                    diagram_object.position[1],
                    diagram_object.size[0],
                    diagram_object.size[1],
                    'Action',
                    None,
                    diagram_object.presentable,
                )
            if isinstance(diagram_object, suite.WhenBranchGE):
                self.add_element(
                    diagram_object.position[0],
                    diagram_object.position[1],
                    diagram_object.label_width,
                    0,
                    'Branch',
                    None,
                    diagram_object.presentable,
                )
            if isinstance(diagram_object, suite.EquationGE):
                equation = diagram_object.equation
                element_type = None
                name = ''
                if equation is not None:
                    element_type = equation.right
                    name = element_type.to_string()
                else:
                    # Emission found
                    pass
                self.add_element(
                    diagram_object.position[0],
                    diagram_object.position[1],
                    diagram_object.size[0],
                    diagram_object.size[1],
                    name,
                    element_type,
                    diagram_object.presentable,
                )

        # then check all edge elements
        for diagram_object in object.presentation_elements:
            if isinstance(diagram_object, suite.Edge):  # just Edge is mistaken by Geographics.Edge
                start_x = 0
                start_y = 0
                first_point = True
                first_line_of_edge = True
                last_line_of_edge = False
                current_line = 0
                number_of_lines = len(diagram_object.points) - 1
                for point in diagram_object.points:
                    if (point[0] == 0) and (point[1] == 0):
                        # TODO: why is that so? Seems like a BUG.
                        error_string = 'False point values for edge: Rule not tested!'
                        if error_string not in self.found_elements:
                            self.found_elements.append(error_string)
                        break
                    if first_point:
                        start_x = point[0]
                        start_y = point[1]
                        first_point = False
                    else:
                        current_line += 1
                        # if two consecutive points are the same, do not test.
                        # line intersection test does not work otherwise
                        if not ((start_x == point[0]) and (start_y == point[1])):
                            if current_line >= number_of_lines:
                                last_line_of_edge = True
                            self._check_line_overlapping(
                                start_x,
                                start_y,
                                point[0] - start_x,
                                point[1] - start_y,
                                diagram_object,
                                first_line_of_edge,
                                last_line_of_edge,
                            )
                            first_line_of_edge = False
                            start_x = point[0]
                            start_y = point[1]

        if len(self.found_elements) > 0:
            number_of_elements = len(self.found_elements)
            sorted_element = sorted(self.found_elements)
            finding_list = '\n'.join(sorted_element)

            self.set_message(
                'Elements overlap ('
                + str(number_of_elements)
                + ') in '
                + object.name
                + ':\n'
                + finding_list
            )
            return Rule.FAILED

        return Rule.OK

    def add_element(self, start_x, start_y, width, height, name_of_element, element_type, target):
        """
        Add a new element to elements list.

        The name of element is used for lines, for example to not test against same element.
        """
        self.g_elements.append(
            GElement(start_x, start_y, width, height, name_of_element, element_type, target)
        )

    def _check_line_overlapping(
        self,
        start_x,
        start_y,
        width,
        height,
        edge: suite.Edge,
        first_line_of_edge: bool,
        last_line_of_edge: bool,
    ):
        start_line_x = 0
        start_line_y = 0
        end_line_x = 0
        end_line_y = 0
        width_line = 0
        height_line = 0

        if width >= 0:
            start_line_x = start_x
            end_line_x = start_x + width
            width_line = width
        else:
            start_line_x = start_x + width
            end_line_x = start_x
            width_line = -width
        if height >= 0:
            start_line_y = start_y
            end_line_y = start_y + height
            height_line = height
        else:
            start_line_y = start_y + height
            end_line_y = start_y
            height_line = -height

        # get name of edge
        name_of_edge = edge.left_var.name

        # get source and destination element of edge
        source_type = None
        destination_type = None
        not_i_source = edge.src_equation.equation
        if isinstance(not_i_source, suite.Equation):
            source_type = not_i_source.right
        else:
            # Emission
            pass
        not_i_destination = edge.dst_equation.equation
        if isinstance(not_i_destination, suite.Equation):
            destination_type = not_i_destination.right

        # get eContainer of edge, can be derived from sourceType or destinationType.
        # Not from variable of edge because the variable can be defined in lower levels.
        # First container is always Equation.

        edge_container = source_type.owner.owner
        container_name = ''

        # check whether edges lie within their own container (States, Actions)
        if isinstance(edge_container, suite.State) or isinstance(edge_container, suite.Action):
            if isinstance(edge_container, suite.Action):
                cont_action = edge_container.owner
                if isinstance(cont_action, suite.WhenBranch):
                    container_name = 'WhenBranch (' + cont_action.pattern.to_string() + '): '
                else:
                    container_name = (
                        'IfAction (' + cont_action.if_node.expression.to_string() + '): '
                    )
            else:
                container_name = edge_container.name
                if container_name != '':
                    container_name += ': '
            # find graphical element within gElements
            for g_element in self.g_elements:
                target = g_element.target
                if not isinstance(target, suite.Edge):
                    # if the containers of edge and target of gElement are equal.
                    # Edge is within a container
                    if edge_container == target:
                        if not (
                            is_point_inside_area(
                                start_line_x,
                                start_line_y,
                                g_element.x,
                                g_element.y,
                                g_element.width,
                                g_element.height,
                            )
                            and is_point_inside_area(
                                end_line_x,
                                end_line_y,
                                g_element.x,
                                g_element.y,
                                g_element.width,
                                g_element.height,
                            )
                        ):
                            ref_link = (
                                '%SC:LOCATE_PATH#'
                                + self._project_name
                                + '#'
                                + edge.get_full_path()
                                + name_of_edge
                                + '/ '
                                + name_of_edge
                                + '%'
                            )
                            error_string = (
                                container_name
                                + 'Edge '
                                + name_of_edge
                                + ' outside box: '
                                + ref_link
                            )
                            if error_string not in self.found_elements:
                                self.found_elements.append(error_string)
                            break

        for g_element in self.g_elements:
            # is gElement Source of Edge
            is_source = False
            # is gElement Destination of Edge
            is_destination = False
            # is gElement line of the same edge
            is_same_edge = False
            # is gElement in the same container or is sub container of this edge
            is_parent = False

            # check whether line belongs to same edge
            is_same_edge = g_element.name_of_element == name_of_edge

            # get elementType. if elementType != null than a SCADE operator with pins is found.
            # If operator belongs to the edge do not test
            g_element_type = g_element.element_type
            if g_element_type is not None:
                if g_element_type == source_type:
                    is_source = first_line_of_edge
                if g_element_type == destination_type:
                    is_destination = last_line_of_edge

            # check whether gElement is parent of edge */
            # get target (means container) of element
            target = g_element.target
            is_edge = isinstance(target, suite.Edge)
            if not is_edge:  # just Edge is mistaken by Geographics.Edge
                # if the containers of edge and gElement are equal gElement cannot be parent.* /
                if not edge_container == target.owner:
                    edge_container_temp = edge_container
                    # check if target is parent of edge container * /
                    while not isinstance(edge_container_temp, suite.Model):
                        if edge_container_temp == target:
                            is_parent = True
                            break
                        edge_container_temp = edge_container_temp.owner

            # do not check lines against lines of the same edge,
            # source element, destination element or parent elements.
            if (
                not is_same_edge
                and not is_source
                and not is_destination
                and not is_parent
                and (self.check_lines or not is_edge)
            ):
                if line_crosses_element(
                    start_line_x, start_line_y, end_line_x, end_line_y, g_element
                ):
                    ref_link = (
                        '%SC:LOCATE_PATH#'
                        + self._project_name
                        + '#'
                        + edge.get_full_path()
                        + name_of_edge
                        + '/ '
                        + name_of_edge
                        + '%'
                    )
                    error_string = (
                        container_name
                        + 'Edge '
                        + name_of_edge
                        + ' crosses '
                        + g_element.name_of_element
                        + ': '
                        + ref_link
                    )
                    if error_string not in self.found_elements:
                        self.found_elements.append(error_string)

        self.g_elements.append(
            GElement(start_line_x, start_line_y, width_line, height_line, name_of_edge, None, edge)
        )


if __name__ == '__main__':
    # rule instantiated outside of a package
    LineCrossing()
