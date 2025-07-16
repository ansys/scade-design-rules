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

"""Implements the CheckConfiguration rule."""

if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.resolve()))


from pathlib import Path

from defusedxml import ElementTree
import scade.model.suite as suite

from ansys.scade.design_rules.utils.rule import Rule


class CheckConfiguration(Rule):
    """Implements the rule interface."""

    def __init__(
        self,
        id='id_0103',
        category='configuration',
        severity=Rule.MANDATORY,
        parameter='conf=KCG,project=check.etp,conf_source=KCG',
        description='Check given configuration against existing project.',
        label='Check configuration',
    ):
        super().__init__(
            id=id,
            category=category,
            severity=severity,
            has_parameter=True,
            default_param=parameter,
            description=description,
            label=label,
            types=[suite.Model],
            kinds=None,
        )

    def on_start(self, model: suite.Model, parameter: str = '') -> int:
        """Get the rule's parameters."""
        d = self.parse_values(parameter)
        if d is None:
            message = f"'{parameter}': parameter syntax error"
        else:
            conf = d.get('conf')
            project = d.get('project')
            conf_source = d.get('conf_source')
            if not conf:
                message = f"'{parameter}': missing 'conf' value"
            elif not project:
                message = f"'{parameter}': missing 'project' value"
            elif not conf_source:
                message = f"'{parameter}': missing 'conf_source' value"
            else:
                self.conf = conf
                # make the path relative to the project
                path = Path(model.descriptor.model_file_name)
                self.project_source_path = path.parent / project
                self.conf_source = conf_source
                return Rule.OK

        self.set_message(message)
        return Rule.ERROR

    def on_check(self, object_: suite.Object, parameter: str = '') -> int:
        """Return the evaluation status for the input object."""
        assert isinstance(object_, suite.Model)  # nosec B101  # addresses linter
        project = object_.project
        configuration = project.find_configuration(self.conf)
        # load source project: nightmare
        # -> scade.load_project can't be used when the rules are evaluated from the IDE
        # -> scade.model.project.project.xml_project.load_project can't be used either
        #    when the rules are evaluated from the IDE (simple typo in the file but enough)
        # the only left option consists in parsing the xml file, with xml since lxml
        # can't be used in the IDE
        try:
            f = self.project_source_path.open()
        except IOError as e:
            self.set_message(str(e))
            return Rule.FAILED
        else:
            _tree = ElementTree.parse(f)
            f.close()

        root = _tree.getroot()

        # find configuration ID of given source configuration
        for element in root.iter():
            if element.tag == 'Configuration':
                id = element.get('id')  # configuration id
                name = element.get('name')  # configuration name
                if name == self.conf_source:
                    conf_id = id
                    break
        else:
            conf_id = -1

        props_source = {}
        # go through all Props
        for element in root.iter():
            if element.tag == 'Prop':
                values = []
                conf_found = False
                # check if configuration matches
                for sub_elem in element.iter():
                    if sub_elem.tag == 'configuration':
                        id = sub_elem.text
                        if id == conf_id:
                            conf_found = True
                    elif sub_elem.tag == 'value':
                        values.append(sub_elem.text)
                # configuration found then compare values
                if conf_found:
                    name = element.get('name')
                    props_source[name] = values

        # get conf settings of current project
        props_target = {_.name: _.values for _ in configuration.props}

        # compare values
        failure_messages = []
        set_props_target = set(props_target)
        set_props_source = set(props_source)
        diff1s = set_props_source - set_props_target
        diff2s = set_props_target - set_props_source
        for diff1 in diff1s:
            failure_messages.append(diff1)
        for diff2 in diff2s:
            if props_target[diff2] != ['']:
                failure_messages.append(diff2)
        for key, value in props_target.items():
            if key in props_source:
                source = props_source[key]
                if value != source:
                    fail_text = f'{key}({",".join(value)} <> {",".join(source)})'
                    failure_messages.append(fail_text)

        if failure_messages:
            self.set_message(f'Configuration not correct: {", ".join(failure_messages)}')
            return Rule.FAILED
        return Rule.OK


if __name__ == '__main__':  # pragma: no cover
    # rule instantiated outside of a package
    CheckConfiguration()
