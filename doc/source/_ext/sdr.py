"""Implements the ``category``, ``rules`` and ``rule`` directives."""

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import unchanged_required
from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective


class Category(nodes.topic, nodes.Element):
    """Category node."""

    pass


def visit_category_node(self, node):
    """Visit a node."""
    self.visit_topic(node)


def depart_category_node(self, node):
    """Start the visit of a node."""
    self.depart_topic(node)


class Categories(nodes.General, nodes.Element):
    """Categories node."""

    pass


def visit_categories_node(self, node):
    """Visit a node."""
    self.visit_general(node)


def depart_categories_node(self, node):
    """Start the visit of a node."""
    self.depart_general(node)


class Rule(nodes.container, nodes.Element):
    """Category node."""

    pass


def visit_rule_node(self, node):
    """Visit a node."""
    self.visit_container(node)


def depart_rule_node(self, node):
    """Start the visit of a node."""
    self.depart_container(node)


class Rules(nodes.General, nodes.Element):
    """``rules`` directive."""

    def __init__(self, filter: str):
        # store the filter for the selected rules
        super().__init__('')
        self.filter = filter


def visit_rules_node(self, node):
    """Visit a node."""
    self.visit_general(node)


def depart_rules_node(self, node):
    """Start the visit of a node."""
    self.depart_general(node)


class CategoriesDirective(Directive):
    """``categories`` directive."""

    def run(self):
        """Return an instance."""
        return [Categories('')]


class CategoryDirective(SphinxDirective):
    """``category`` directive."""

    # this enables content in the directive
    has_content = True

    option_spec = {'name': unchanged_required}

    def run(self):
        """Return an instance."""
        targetid = 'sdr-%d' % self.env.new_serialno('sdr')
        targetnode = nodes.target('', '', ids=[targetid])

        category_node = Category('\n'.join(self.content))
        category_node += nodes.title(_('Description'), _('Description'))
        self.state.nested_parse(self.content, self.content_offset, category_node)
        children = category_node.children
        if len(children) == 1:
            # contains only the title added above, no description:
            # stub it
            category_node += nodes.Text(_('<TODO Description>'))

        if not hasattr(self.env, 'sdr_categories'):
            self.env.sdr_categories = []

        self.env.sdr_categories.append(
            {
                'docname': self.env.docname,
                'lineno': self.lineno,
                'target': targetnode,
                'name': self.options['name'],
                'description': children[1].deepcopy(),
            }
        )

        return [targetnode, category_node]


class RulesDirective(Directive):
    """``rules`` directive."""

    has_content = False

    option_spec = {
        'filter': unchanged_required,
    }

    def run(self):
        """Return an instance."""
        return [Rules(self.options['filter'])]


class RuleDirective(SphinxDirective):
    """``rule`` directive."""

    # this enables content in the directive
    has_content = True

    option_spec = {
        'filename': unchanged_required,
        'class': unchanged_required,
        'id': unchanged_required,
        'reference': unchanged_required,
        'tags': unchanged_required,
        'kind': unchanged_required,
    }

    def run(self):
        """Return an instance."""
        targetid = 'sdr-%d' % self.env.new_serialno('sdr')
        targetnode = nodes.target('', '', ids=[targetid])

        label_id = nodes.make_id('Rule' + self.options['class'])
        self.env.app.env.domaindata['std']['anonlabels'][label_id] = self.env.docname, label_id

        rule_node = Rule('\n'.join(self.content), ids=[label_id])
        self.state.nested_parse(self.content, self.content_offset, rule_node)
        if not rule_node.children:
            # no short description: stub it
            rule_node += nodes.Text(_('<TODO Description>'))

        if not hasattr(self.env, 'sdr_rules'):
            self.env.sdr_rules = []

        self.env.sdr_rules.append(
            {
                'docname': self.env.docname,
                'lineno': self.lineno,
                'target': targetnode,
                'props': self.options,
                'description': rule_node.children[0].deepcopy(),
            }
        )

        return [targetnode, rule_node]


def purge_categories(app, env, docname):
    """Implement env-purge-doc for categories."""
    if not hasattr(env, 'sdr_categories'):
        return

    env.sdr_categories = [_ for _ in env.sdr_categories if _['docname'] != docname]


def merge_categories(app, env, docnames, other):
    """Implement env-merge-info for categories."""
    if not hasattr(env, 'sdr_categories'):
        env.sdr_categories = []

    if hasattr(other, 'sdr_categories'):
        env.sdr_categories.extend(other.sdr_categories)


def purge_rules(app, env, docname):
    """Implement env-purge-doc for rules."""
    if not hasattr(env, 'sdr_rules'):
        return

    env.sdr_rules = [_ for _ in env.sdr_rules if _['docname'] != docname]


def merge_rules(app, env, docnames, other):
    """Implement env-merge-info for rules."""
    if not hasattr(env, 'sdr_sdr_rules'):
        env.sdr_sdr_rules = []

    if hasattr(other, 'sdr_rules'):
        env.sdr_rules.extend(other.sdr_rules)


def process_category_nodes(app, doctree, fromdocname):
    """
    Replace all categories nodes with a list of the collected categories.

    Augment each category with a back-link to the original location.
    """
    env = app.builder.env

    if not hasattr(env, 'sdr_categories'):
        env.sdr_categories = []

    for node in doctree.findall(Categories):
        table = nodes.table()
        tgroup = nodes.tgroup(cols=2)
        for i in range(2):
            colspec = nodes.colspec(colwidth=1)
            tgroup.append(colspec)
        table += tgroup

        # thead = nodes.thead()
        # tgroup += thead
        # row = nodes.row()
        # entry = nodes.entry()
        # entry += nodes.paragraph(text="Name")
        # row += entry
        # entry = nodes.entry()
        # entry += nodes.paragraph(text="Description")
        # row += entry
        #
        # thead.append(row)

        rows = []

        category_infos = sorted(env.sdr_categories, key=lambda _: _['name'])
        for category_info in category_infos:
            row = nodes.row()
            rows.append(row)

            refnode = nodes.reference(text=category_info['name'])
            refnode['refdocname'] = category_info['docname']
            refnode['refuri'] = app.builder.get_relative_uri(fromdocname, category_info['docname'])
            refnode['refuri'] += '#' + category_info['target']['refid']
            entry = nodes.entry()
            para = nodes.paragraph()
            entry += para
            para += refnode
            row += entry

            entry = nodes.entry()
            entry += category_info['description']
            row += entry

        tbody = nodes.tbody()
        tbody.extend(rows)
        tgroup += tbody

        node.replace_self(table)


def process_rule_nodes(app, doctree, fromdocname):
    """
    Replace all categories nodes with a list of the collected categories.

    Augment each category with a back-link to the original location.
    """
    env = app.builder.env

    if not hasattr(env, 'sdr_rules'):
        env.sdr_rules = []

    for node in doctree.findall(Rules):
        labels = ['Name', 'ID', 'Ref', 'Synopsis']

        table = nodes.table()
        tgroup = nodes.tgroup(cols=len(labels))
        for i in range(len(labels)):
            colspec = nodes.colspec(colwidth=1)
            tgroup.append(colspec)
        table += tgroup

        thead = nodes.thead()
        tgroup += thead
        row = nodes.row()
        for label in labels:
            entry = nodes.entry()
            entry += nodes.paragraph(text=label)
            row += entry

        thead.append(row)

        rows = []

        # rule_infos = env.sdr_rules
        rule_infos = sorted(env.sdr_rules, key=lambda _: _['props']['class'])
        for rule_info in rule_infos:
            tags = rule_info['props']['tags'].split()
            if node.filter != '*' and node.filter not in tags:
                continue
            row = nodes.row()
            rows.append(row)

            refnode = nodes.reference(text=rule_info['props']['class'])
            refnode['refdocname'] = rule_info['docname']
            refnode['refuri'] = app.builder.get_relative_uri(fromdocname, rule_info['docname'])
            refnode['refuri'] += '#' + rule_info['target']['refid']
            entry = nodes.entry()
            para = nodes.paragraph()
            entry += para
            para += refnode
            row += entry

            entry = nodes.entry()
            para = nodes.paragraph()
            entry += para
            para += nodes.Text(rule_info['props']['id'])
            row += entry

            entry = nodes.entry()
            para = nodes.paragraph()
            entry += para
            para += nodes.Text(rule_info['props']['reference'])
            row += entry

            entry = nodes.entry()
            entry += rule_info['description']
            row += entry

        tbody = nodes.tbody()
        tbody.extend(rows)
        tgroup += tbody

        node.replace_self(table)


def setup(app):
    """Declare the nodes and directives."""
    app.add_node(
        Categories,
        html=(visit_categories_node, depart_categories_node),
        latex=(visit_categories_node, depart_categories_node),
        text=(visit_categories_node, depart_categories_node),
    )
    app.add_node(
        Category,
        html=(visit_category_node, depart_category_node),
        latex=(visit_category_node, depart_category_node),
        text=(visit_category_node, depart_category_node),
    )
    app.add_node(
        Rules,
        html=(visit_rules_node, depart_rules_node),
        latex=(visit_rules_node, depart_rules_node),
        text=(visit_rules_node, depart_rules_node),
    )
    app.add_node(
        Rule,
        html=(visit_rule_node, depart_rule_node),
        latex=(visit_rule_node, depart_rule_node),
        text=(visit_rule_node, depart_rule_node),
    )

    app.add_directive('category', CategoryDirective)
    app.add_directive('categories', CategoriesDirective)
    app.connect('doctree-resolved', process_category_nodes)
    app.connect('env-purge-doc', purge_categories)
    app.connect('env-merge-info', merge_categories)
    app.add_directive('rule', RuleDirective)
    app.add_directive('rules', RulesDirective)
    app.connect('doctree-resolved', process_rule_nodes)
    app.connect('env-purge-doc', purge_rules)
    app.connect('env-merge-info', merge_rules)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
