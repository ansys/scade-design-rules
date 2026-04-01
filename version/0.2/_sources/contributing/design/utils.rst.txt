Utilities
#########

The ``./src/ansys/scade/design_rules/utils`` directory contains Python
components to ease the development of metrics and rules.

The most important ones are the ``Metric`` and ``Rule`` classes which must
be derived by all the metrics and rules defined in the repository.

The first objective of these classes is to provide a stub for the
top-level ``class scade.tool.suite.rules.Metric`` and ``class scade.tool.suite.rules.Rule``
when unit testing or debugging the rules outside the context of *SCADE Metrics and Rules Checker*.

The following sections describe the interface of the ``Rule`` class and its services.

The class ``Metric`` has a similar but simpler design.

Stubs
=====

The class stubs the ``set_message`` method and stores the parameter in ``self.message``.
This is for testing purposes.

Parameter
=========

The ``parse_values`` method compiles a parameter string made of comma separated fields ``<name>=<value>``.
It returns the elements and their value as a dictionary.

Kinds
=====
The new ``Rule`` class has the same interface as its top-level one plus an additional ``kinds`` parameter.
The purpose of this parameter is to provide an alternative to the  ``types`` parameter.

Indeed,  ``types`` specifies a list of Python classes, but several objects of the same class
may have different usages or semantics. For example, enumeration values or constants are both
instances of ``scade.model.suite.Constant``, and it should be possible to have rules only for
enumeration values or only for constants.

Thus, it is possible for a rule to register to kinds instead of types. Such rules
must define a ``on_check_ex`` function instead of ``on_check``.

The available kinds are defined by a class and a filter:

.. code::

  class SCK(Enum):
    MODEL = (suite.Model, lambda o: True)
    PACKAGE = (suite.Package, lambda o: not isinstance(o, suite.Model))
    TYPE = (suite.NamedType, lambda o: not (o.is_predefined() or o.is_generic()))
    GENERIC_TYPE = (suite.NamedType, lambda o: o.is_generic())
    FIELD = (suite.CompositeElement, lambda o: True)
    SENSOR = (suite.Sensor, lambda o: True)
    CONSTANT = (suite.Constant, lambda o: isinstance(o.owner, suite.Package))
    ENUM_VALUE = (suite.Constant, lambda o: isinstance(o.owner, suite.Enumeration))
    PARAMETER = (suite.Constant, lambda o: isinstance(o.owner, suite.Operator))
    OPERATOR = (suite.Operator, lambda o: True)
    VARIABLE = (suite.LocalVariable, lambda o: o.is_local() and not o.is_internal())
    INPUT = (suite.LocalVariable, lambda o: o.is_input())
    HIDDEN = (suite.LocalVariable, lambda o: o.is_hidden())
    OUTPUT = (suite.LocalVariable, lambda o: o.is_output())
    SIGNAL = (suite.LocalVariable, lambda o: o.is_signal())
    INTERNAL = (suite.LocalVariable, lambda o: o.is_internal())
    DIAGRAM = (suite.Diagram, lambda o: not isinstance(o, suite.TreeDiagram))
    EQ_SET = (suite.EquationSet, lambda o: True)
    STATE_MACHINE = (suite.StateMachine, lambda o: True)
    STATE = (suite.State, lambda o: True)
    IF_BLOCK = (suite.IfBlock, lambda o: True)
    WHEN_BLOCK = (suite.WhenBlock, lambda o: True)

Reporting
=========
A rule can subscribe and raise violations for any Scade model element,
including graphical objects or expressions.
However, these items do not have an OID and it is not possible, for example,
to create justifications for such violations.

*SCADE Metrics and Rules Checker* 2024 R2 provides an enhancement so that a rule
can declare a violation for an element, and provide an OID associated to a
local one determined by the rule itself.
This is achieved with the ``add_rule_status`` method.

For example, consider a rule that checks that the wires don't have more
than 4 intermediate points. This rule can register to equations and always
return ``Rule.NA``. It checks all the outgoing edges of the equation and
reports each violation using ``add_rule_status`` with the equation's OID and
the name of the edge's local variable as local OID.

The ``Rule`` class provides support for this use case.

* ``add_rule_status``: This method is redefined to address both
  *SCADE Metrics and Rules Checker* 2024 R2 and former releases.
  The ``local_id`` parameter is discarded for former releases.

  Moreover, this method maintains, in a cache, a dictionary of these violations
  to prevent duplicated violations. This eases the development of rules in
  some circumstances.
* ``on_stop``: This method empties the cache of violations. It must be called
  if it is overridden in derived classes.
* ``get_closest_annotatable``: This method returns the closest owner that
  has an OID, for an element. This allows rules to subscribe to low-level
  elements, such as expressions, and raise a violation for their closest
  container.
