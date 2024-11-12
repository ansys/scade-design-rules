.. index:: single: Forbidden Operators

Forbidden Operators
===================

.. rule::
   :filename: forbidden_operators.py
   :class: ForbiddenOperators
   :id: id_0023
   :reference: n/a
   :kind: generic
   :tags: modelling

   Forbidden Operators

Description
-----------

.. start_description

Specific predefined SCADE operators shall not be used: merge (45) and When (28).
parameter: comma separated list of operator IDs, for example.: 45,28

.. end_description

The rule parameter is a comma-separated string containing predefined operator identifiers.
Available identifiers are documented in the SCADE Python API guide, under section *Access to Predefined Operators in Python*.
Default parameter value is ``45, 28`` (Merge, When).

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that a given list of predefined operators is avoided in diagrams.

The default value of the rule parameter prevents use of the Merge and When operators, that are not intended for direct use and are hidden from toolbars by default in the SCADE editor.

Note: this is a stronger version of rule :ref:`Disadvised Operators <RuleDisadvisedOperators>`: its severity is ``REQUIRED``.

Verification
------------
This rule checks all operator calls in a model and fails if one of the operators in the parameter list is called.

Resolution
----------
Modify the offending operator calls as detailed in the rule failure message.

Customization
-------------
N/A.

.. seealso::
  * Rule :ref:`Disadvised Operators <RuleDisadvisedOperators>`
