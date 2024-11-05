.. index:: single: No Operatorcalls In Expressions

No Operatorcalls In Expressions
===============================

.. rule::
   :filename: no_operatorcalls_in_expressions.py
   :class: NoOperatorCallsInExpressions
   :id: id_0060
   :reference: n/a
   :kind: generic
   :tags: modelling

   No operator calls in expressions

Description
-----------

.. start_description

No operator calls within textual expressions.
This rule does not apply for Constants and Transition/IfNode conditions.
Exceptions on main level can be given as parameters.
parameter: operator IDs separated by comma: e.g.: '18,...'

.. end_description

The rule parameter is a comma-separated string containing predefined operators identifiers that are allowed to be called from within textual expressions.
Available identifiers are documented in the SCADE Python API guide, under section "Access to Predefined Operators in Python". Default value is ``18`` (array projection operator).

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that textual expressions do not contain operator calls.

One use case for this could be to guarantee model readability for mixed teams of software engineers
(who are comfortable with both diagrams and textual programs) and system engineers (who are less comfortable with textual programs).

Verification
------------
This rule checks all operator calls throughout the model. The rule fails if it finds an operator calls that is part of a textual expression
and that is **not** part of the list of authorized operators.

Resolution
----------
Modify the offending textual expression to remove the offending call, or reimplement it as a graphical diagram.

Customization
-------------
N/A.
