.. index:: single: Not Recommended Operators

Not Recommended Operators
=========================

.. rule::
   :filename: disadvised_operators.py
   :class: DisadvisedOperators
   :id: id_0013
   :reference: n/a
   :kind: generic
   :tags: modelling

   Not Recommended Operators

Description
-----------

.. start_description

Specific predefined SCADE operators should not be used: reverse (46), transpose (47), slice (51), Concatenation (52)

.. end_description

The rule parameter is a comma-separated string containing predefined operator identifiers.
Available identifiers are documented in the SCADE Python API guide, under section *Access to Predefined Operators in Python*.
Default parameter value is ``46, 47, 51, 52`` (Reverse, Transpose, Slice, Concatenation).

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that a given list of predefined operators is avoided in diagrams.

Note: this is a lighter version of rule :ref:`Forbidden Operators <RuleForbiddenOperators>`: its severity is ``ADVISORY``.

Verification
------------
This rule checks all operator calls in a model and fails if one of the listed operators is used.

Resolution
----------
Modify the offending operator calls as detailed in the rule failure message.

Customization
-------------
N/A.

.. seealso::
  * Rule :ref:`Forbidden Operators <RuleForbiddenOperators>`
