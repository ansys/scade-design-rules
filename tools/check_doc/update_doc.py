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

"""Check there is one doc per rule and vice versa."""

__author__ = 'Jean Henry'

# import docutils.nodes
# import docutils.parsers.rst
# import docutils.utils
# import docutils.frontend
import importlib
from pathlib import Path
import re
import sys

import jinja2

environment = None


def filter_underline(text: str, char: str) -> str:
    return text + '\n' + char * len(text)


def create_category(dir: Path, context):
    model = 'content.rst'
    try:
        template = environment.get_template(model)
    except BaseException as e:
        print(e)
        return
    dir.mkdir(exist_ok=True)
    text = template.render(context)
    file = dir / model
    with file.open('w') as f:
        f.write(text)
    print('creating', file)
    return dir


def create_rule(file: Path, context):
    model = 'rule.rst'
    try:
        template = environment.get_template(model)
    except BaseException as e:
        print(e)
        return
    file.parent.mkdir(exist_ok=True)
    text = template.render(context)
    with file.open('w') as f:
        f.write(text)
    print('creating', file)
    return file


# Example from https://stackoverflow.com/questions/12883428/how-to-parse-restructuredtext-in-python
# def parse_rst(text: str) -> docutils.nodes.document:
#     parser = docutils.parsers.rst.Parser()
#     settings = docutils.frontend.get_default_settings(docutils.parsers.rst.Parser)
#     document = docutils.utils.new_document('<rst-doc>', settings=settings)
#     parser.parse(text, document)
#     return document

rerule = re.compile(r'..\s+rule\s*::')
reclass = re.compile(r'(\s*:class:\s*).*')
reid = re.compile(r'(\s*:id:\s*).*')


def update_rule(file: Path, rule) -> bool:
    # update the fields class, id, label and description from rule
    ok = True

    # quick and dirty parser: not able to use parse_rst
    # doc = parse_rst(file.open().read())

    # fix common mistake with md/rst
    # escape trailing '_'
    description = re.sub(r"(\w+)_( |$|,|')", r'\1\\_\2', rule.description)
    description = description.split('\n')
    for i in range(1, len(description)):
        if (
            description[i]
            and description[i][0] == '*'
            and (not description[i - 1] or description[i - 1][0] != '*')
        ):
            description[i - 1] += '\n'
    # make the lines consistent
    description = '\n'.join(description).split('\n')

    lines = file.open().read().split('\n')
    newlines = []
    marker = None
    mode = 'idle'
    buffer = []
    for i, line in enumerate(lines):
        if mode == 'rule':
            m = reclass.fullmatch(line)
            if m:
                line = m.groups()[0] + type(rule).__name__
            else:
                m = reid.fullmatch(line)
                if m:
                    line = m.groups()[0] + rule.id
                elif line.strip() == '':
                    mode = 'rule_label'
        elif mode == 'rule_label':
            if line and line[0] != ' ':
                # flush rule's label (TODO: compute indentation)
                newlines.extend(['   ' + _ for _ in rule.label.split('\n')])
                newlines.append('')
                mode = 'idle'
            else:
                # skip line
                continue
        elif mode == 'descr':
            if not marker:
                # -*
                marker = line

            if line == 'Rationale' and lines[i + 1][0] == '-' or line == '.. end_description':
                # allow using .. end_description without .. start_description
                # flush title marker, rule's description
                newlines.append(marker)
                newlines.extend(description)
                newlines.append('')
                mode = 'done'
            elif line == '.. start_description':
                # only a part of the description shall be updated
                # flush the buffered lines
                newlines.extend(buffer)
                mode = 'descr_area'
            elif line == '.. preserve_description':
                # the description shall not be updated
                # flush the buffered lines
                newlines.extend(buffer)
                mode = 'done'
            else:
                buffer.append(line)
                continue
        elif mode == 'descr_area':
            if line == '.. end_description':
                # flush rule's description
                newlines.append('')
                newlines.extend(description)
                newlines.append('')
                mode = 'done'
            else:
                continue

        if mode == 'idle':
            if line == 'Description' and lines[i + 1][0] == '-':
                # buffer the lines
                mode = 'descr'
            elif line == '.. rule::':
                mode = 'rule'

        newlines.append(line)

    if mode == 'descr_area':
        ok = False
        print("%s: '.. end description' not found" % file.name)
    elif mode == 'descr':
        ok = False
        print("%s: 'Rationale' not found" % file.name)
    elif mode != 'done':
        ok = False
        print('%s: parse error' % file.name)
    else:
        # flush the file
        if newlines[-1] != '':
            # make sure the file ends with an emptyline
            newlines.append('')
        if newlines != lines:
            print('updating', file)
            file.open('w').write('\n'.join(newlines))
            ok = False

    return ok


# __init__ replacement function to store the
# parameters as attributes
def local_init(c, **kwargs):
    for name, value in kwargs.items():
        setattr(c, name, value)


def rule_instance(module: str):
    module = 'ansys.scade.design_rules.' + module
    base_name = module.split('.')[-1]

    m = importlib.import_module(module)

    rule_class = getattr(m, 'Rule')
    rule_class.__init__ = local_init

    class_name = ''.join([_.capitalize() for _ in base_name.split('_')])
    try:
        class_ = getattr(m, class_name)
    except BaseException:
        class_ = None
    if not class_:
        # try to find a class with an identical name, case insensitive
        for attr, value in m.__dict__.items():
            if attr.lower() == class_name.lower():
                class_ = value
                break
            elif isinstance(value, rule_class):
                # hope there is only one rule in the file
                print('warning: considering %s instead of %s' % (attr, class_name))
                class_ = value
                break
        else:
            print('%s.%s: class error' % (module, class_name))
            return None
    return class_()


def update_doc(root: Path) -> int:
    global environment

    exit_code = 0
    # load auto_scade_env
    try:
        importlib.__import__('ansys.scade.apitools')
    except BaseException:
        exit_code = 1
        print('apitools', 'import error')
        return exit_code

    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(root / 'doc' / '_templates'))
    )
    environment.filters['underline'] = filter_underline

    rules_dir = 'doc/source/rules/'
    srcs = sorted(
        [
            _
            for _ in root.glob('src/ansys/scade/design_rules/*')
            if _.is_dir() and _.name != 'utils' and _.name != '__pycache__'
        ]
    )
    docs = {_.name: _ for _ in root.glob(rules_dir + '*') if _.is_dir()}
    for src in srcs:
        try:
            doc = docs.pop(src.name)
        except KeyError:
            print('%s: no doc directory' % src.name)
            doc = None
        if not doc or not (doc / 'content.rst').exists():
            exit_code = 1
            name = src.name
            context = {
                'filter': name,
                'title': ' '.join([_.capitalize() for _ in name.split('_')]),
            }
            doc = create_category(root / rules_dir / src.name, context)
        rsts = {_.stem.lower(): _ for _ in doc.glob('*.rst') if _.stem.lower() != 'content'}
        rules = sorted([_ for _ in src.glob('*.py') if _.name != '__init__.py'])
        for rule in rules:
            name = rule.stem
            # create an instance of the rule to get its attributes
            instance = rule_instance('%s.%s' % (src.name, rule.stem))
            if not instance:
                exit_code = 1
                continue
            if name.lower() in rsts:
                rst_file = rsts.pop(name.lower())
                if not update_rule(rst_file, instance):
                    exit_code = 1
            else:
                exit_code = 1
                print('%s/%s: no rst file' % (doc.name, rule.name))
                # create a default rst file from the template
                if instance:
                    context = {
                        'title': ' '.join([_.capitalize() for _ in name.split('_')]),
                        'file': rule.name,
                        'class': type(instance).__name__,
                        'category': doc.stem,
                        'rule': instance,
                    }
                    create_rule(doc / rule.with_suffix('.rst').name, context)
        for rst in sorted(rsts.keys()):
            exit_code = 1
            print('%s/%s: no rule' % (doc.name, rsts[rst].name))

    return exit_code


if __name__ == '__main__':
    # dir must be the root of the repository
    dir = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).parent.parent.parent
    sys.path.append(str(dir / 'src'))
    sys.exit(update_doc(dir))
