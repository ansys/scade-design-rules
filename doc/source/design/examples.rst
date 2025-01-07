Examples
========

Design
------
The examples are intended to showcase easily the usage of a metric or rule.
They shall be configured to refer to their corresponding rule using
relative paths, for example:

.. image:: /_static/declare_rule.png
   :alt: Declare a rule for *Metrics and Rules Checker*

When a rule's behavior depends on a parameter, the example can define several
configurations for *Metrics and Rules Checker* to demonstrate the alternatives.

The examples are located in the directory ``./examples``.
The structure of this directory must match the structure of ``./src/ansys/scade/design_rules``.

Tools
-----
The ``pre-commit`` hook ``check_models`` ensures there is one example per rule.
It issues a warning if an example does not correspond to a rule.
This a light verification based on naming rules.
