.. index:: single: Has Link Or Part Of Equation Set

Has Link Or Part Of Equation Set
================================

.. rule::
   :filename: has_link_or_part_of_equation_set.py
   :class: HasLinkOrPartOfEquationSet
   :id: id_0026
   :reference: n/a
   :kind: specific
   :tags: traceability

   Has traceability link

Description
-----------

.. start_description

This rule checks if the elements have traceability links via the ALM Gateway or is part of an Equation Set

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that all model elements
that are not part of an equation set are traced to high-level requirements.

This is a variation of rule :ref:`Has Link <RuleHasLink>`.

Verification
------------
This rules checks all constants, operators, diagrams, and equation sets throughout the model.

The rule fails if it finds an element with no linked requirement.

Note: equation sets themselves must be linked to requirements.

Resolution
----------
Link the offending element to a requirement using the ALM Gateway.

Customization
-------------
TODO

.. seealso::
  * Rule :ref:`Has Link <RuleHasLink>`
