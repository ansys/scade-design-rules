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

"""
Performs checks and updates the documentation from the metrics and rules.

* Checks there is one documentation file per metric/rule and vice versa.
* Creates a default index file for new categories.
* Creates a default documentation file for new metrics and rules.
* Updates the documentation with the rule's properties: description, etc.
* Updates ``./src/ansys/scade/design_rules/catalog.txt``.
"""

import importlib
from pathlib import Path
import re
import sys
from typing import Any

from jinja2 import Environment, FileSystemLoader
from rich import print

environment = None


def filter_underline(text: str, char: str) -> str:
    """Return the underline string for a text."""
    return text + '\n' + char * len(text)


def create_category(dir: Path, context) -> None | Path:
    """Create a new documentation category from a template."""
    assert environment
    model = 'category.rst'
    try:
        template = environment.get_template(model)
    except BaseException as e:
        print(f'[red]{e}[/red]')
        return None
    dir.mkdir(exist_ok=True)
    text = template.render(context)
    file = (dir / model).with_stem('index')
    file.write_text(text)
    print(f'[red]Creating, {file}[/red]')
    return dir


def create_rst(file: Path, context, model: str) -> None | Path:
    """Create a new documentation file from a template."""
    assert environment
    try:
        template = environment.get_template(model)
    except BaseException as e:
        print(f'[red]{e}[/red]')
        return None
    file.parent.mkdir(exist_ok=True)
    text = template.render(context)
    file.write_text(text)
    print(f'[red]Creating {file}[/red]')
    return file


reclass = re.compile(r'(\s*:class:\s*).*')
reid = re.compile(r'(\s*:id:\s*).*')


def update_rst(file: Path, instance, kind: str) -> bool:
    """Update the fields class, id, label and description from a metric or rule."""
    ok = True

    # quick and dirty parser: not able to use parse_rst
    # doc = parse_rst(file.open().read())

    # fix common mistake with md/rst
    # escape trailing '_'
    description = re.sub(r"(\w+)_( |$|,|')", r'\1\\_\2', instance.description)
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

    lines = file.read_text().split('\n')
    newlines = []
    marker = None
    mode = 'idle'
    buffer = []
    n = len(lines)
    for i, line in enumerate(lines):
        if mode == 'metric_rule':
            m = reclass.fullmatch(line)
            if m:
                line = m.groups()[0] + type(instance).__name__
            else:
                m = reid.fullmatch(line)
                if m:
                    line = m.groups()[0] + instance.id
                elif line.strip() == '':
                    mode = 'rule_label'
        elif mode == 'rule_label':
            if line and line[0] != ' ':
                # flush label (TODO: compute indentation)
                newlines.extend(['   ' + _ for _ in instance.label.split('\n')])
                newlines.append('')
                mode = 'idle'
            else:
                # skip line
                continue
        elif mode == 'descr':
            if not marker:
                # -*
                marker = line

            if (i < n - 1 and lines[i + 1] == '=' * len(lines[i])) or line == '.. end_description':
                # allow using .. end_description without .. start_description
                # flush title marker, description
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
                # flush description
                newlines.append('')
                newlines.extend(description)
                newlines.append('')
                mode = 'done'
            else:
                continue

        if mode == 'idle':
            if line == 'Description' and lines[i + 1][0] == '=':
                # buffer the lines
                mode = 'descr'
            elif line == f'.. {kind}::':
                mode = 'metric_rule'

        newlines.append(line)

    if mode == 'descr_area':
        ok = False
        print(f"[red]Error: '.. end description' not found for {file.name}[/red]")
    elif mode == 'descr':
        ok = False
        print(f"[red]Error: next section after 'description' not found for {file.name}[/red]")
    elif mode != 'done':
        ok = False
        print(f'[red]Error: parse error for {file.name}[/red]')
    else:
        # flush the file
        if newlines[-1] != '':
            # make sure the file ends with an emptyline
            newlines.append('')
        if newlines != lines:
            print(f'[red]Error: Updating, {file}[/red]')
            file.open('w').write('\n'.join(newlines))
            ok = False

    return ok


def local_init(c, **kwargs):
    """
    Store the parameters as attributes.

    This function replaces the rules' ``__init__`` method.
    """
    for name, value in kwargs.items():
        setattr(c, name, value)


def metric_rule_instance(module: str) -> Any:
    """Create an instance of a rule."""
    module = 'ansys.scade.design_rules.' + module
    base_name = module.split('.')[-1]

    m = importlib.import_module(module)

    # should be either a rule or a metric
    rule_metric_class_ = getattr(m, 'Rule', None)
    if not rule_metric_class_:
        rule_metric_class_ = getattr(m, 'Metric', None)
    if not rule_metric_class_:
        print(f'[red]Error: no metric/rule found in {module}[/red]')
        return None

    rule_metric_class_.__init__ = local_init

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
            elif isinstance(value, rule_metric_class_):
                # hope there is only one rule in the file
                print(f'[yellow]Warning: considering {attr} instead of {class_name}[/yellow]')
                class_ = value
                break
        else:
            print(f'[red]Class error: {module}.{class_name} class was not found[/red]')
            return None
    return class_()


def update_doc(root: Path) -> int:
    """Check and update the documentation with respect to the sources."""
    global environment

    exit_code = 0
    # load auto_scade_env
    try:
        importlib.__import__('ansys.scade.apitools')
    except BaseException:
        exit_code = 1
        print('[red]ansys.scade.apitools could not be imported[/red]')
        return exit_code

    # catalog of rules: (id, category, class)
    catalog: list[tuple[str, str, str]] = []

    environment = Environment(loader=FileSystemLoader(str(root / 'doc' / '_templates')))
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
    # add the metrics directory
    docs['metrics'] = root / 'doc/source/metrics'
    for src in srcs:
        try:
            doc = docs.pop(src.name)
        except KeyError:
            print(f'[red]Error: no doc directory for {src.name} rule set[/red]')
            doc = None
        if doc is None or not (doc / 'index.rst').exists():
            exit_code = 1
            name = src.name
            # rules only
            assert name != 'metrics'
            context = {
                'filter': name,
                'title': name.title().replace('_', ' '),
            }
            doc = create_category(root / rules_dir / name, context)
        if doc is None:
            continue
        rsts = {_.stem.lower(): _ for _ in doc.glob('*.rst') if _.stem.lower() != 'index'}
        rules = sorted([_ for _ in src.glob('*.py') if _.name != '__init__.py'])
        for rule in rules:
            name = rule.stem
            # create an instance of the rule to get its attributes
            instance = metric_rule_instance(f'{src.name}.{rule.stem}')
            # metric_rule_instance could return `kind` instead of relying on some attribute
            kind = 'rule' if hasattr(instance, 'severity') else 'metric'
            if not instance:
                exit_code = 1
                continue
            if name.lower() in rsts:
                rst_file = rsts.pop(name.lower())
                if not update_rst(rst_file, instance, kind):
                    exit_code = 1
            else:
                exit_code = 1
                print(f'[red]Error: no rst file found for {doc.name}/{rule.name} rule[/red]')
                # create a default rst file from the template
                if instance:
                    tokens = name.split('_')
                    # the attributes are common for rules and metrics
                    context = {
                        'title': ' '.join([tokens[0].capitalize()] + tokens[1:]),
                        'file': rule.name,
                        'class': type(instance).__name__,
                        'category': doc.stem,
                    }
                    context[kind] = instance
                    model = f'{kind}.rst'
                    create_rst(doc / rule.with_suffix('.rst').name, context, model)
            # update the catalog
            catalog.append((instance.id, src.name, rule.stem))
        for rst in sorted(rsts.keys()):
            exit_code = 1
            print(f'[red]Error: No rule found for {doc.name}/{rsts[rst].name} doc file[/red]')

    # write the catalog
    catalog.sort(key=lambda t: t[0])
    catalog_path = root / 'src/ansys/scade/design_rules' / 'catalog.txt'
    with catalog_path.open('w') as file:
        file.write('id\tcategory\tname\n')
        for id, category, name in catalog:
            file.write(f'{id}\t{category}\t{name}\n')

    return exit_code


if __name__ == '__main__':
    from ansys.scade.apitools import declare_project

    if declare_project is None:
        # scade not installed on the runner, skip the check
        sys.exit(0)
    # dir must be the root of the repository
    dir = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).parent.parent.parent
    sys.path.append(str(dir / 'src'))
    sys.exit(update_doc(dir))
