User guide
==========
Ansys SCADE Design Rules is a database of metrics and rules that enforce various design practices on a model.

While it is possible to individually reference each rule to add them to a SCADE project,
a common practice is to instantiate a selection of rules in one Python script,
and then register that script to the project.

This tutorial presents the basic steps to setup such a collection of rules for a SCADE Suite project.
Note that a SCADE project may use several collections of rules.

Rules
-----
Browse or search the documentation for the rules you want to use.

For example, consider the following naming rules:

* :ref:`CamelCaseNaming <RuleCamelCaseNaming>`
* :ref:`PascalCaseNaming <RulePascalCaseNaming>`
* :ref:`UpperCaseNaming <RuleUpperCaseNaming>`

The name of the python module corresponding to a rule is derived from the *pythonization*
of its name and category.
The words are lowered and separated with ``_``.

For example, the Python module defining the rule ``CamelCaseNaming``, from the category ``Naming``,
is ``ansys.scade.design_rules.naming.camel_case_naming``.

Instantiation
-------------
Each rule is implemented as a Python class.
Once the rules have been identified, create a Python script that instantiates their classes.
This script can be saved anywhere on your file system.

.. literalinclude :: resources/naming_default.py

.. _ug_customization:

Customization
-------------
The rules have default properties that can be overridden at instantiation.
The following properties are available for every rule:

* id
* label
* category
* severity
* description

Refer to the section *Rule Class Methods* of the SCADE Suite documentation for details.
Some rules allows overriding other properties, such as ``types`` or ``parameter``.
Refer to the *Customization* section of their documentation for details.

For example:

.. literalinclude :: resources/naming_custom.py

Rules that depend on metrics provide an additional property, usually ``metric_id``,
to specify an alternate metric.

For example:

.. literalinclude :: resources/metric_custom.py

Registration
------------
Register the script as described in the section *Managing Project Metrics and Rules* of the SCADE Suite documentation.

Note that Ansys SCADE 2024 R2 can also access rules from installed Python packages.
