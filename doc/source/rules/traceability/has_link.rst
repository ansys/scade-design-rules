.. index:: single: Has link

Has link
========

.. rule::
   :filename: has_link.py
   :class: HasLink
   :id: id_0025
   :reference: n/a
   :kind: specific
   :tags: traceability

   Has traceability link

Description
-----------

.. start_description

This rule checks if the elements have traceability links via the ALM Gateway.

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring
that all model elements are traced to high-level requirements.

This is a variation of rule :ref:`Has Link Or Part Of Equationset <RuleHasLinkOrPartOfEquationSet>`.

Verification
------------
This rules checks all constants, operators, diagrams, and equation sets throughout the model.

The rule fails if it finds an element with no linked requirement.

Resolution
----------
Link the offending element to a requirement using the ALM Gateway.

Customization
-------------
TODO

.. seealso::
  * Rule :ref:`Has Link Or Part Of Equationset <RuleHasLinkOrPartOfEquationSet>`
