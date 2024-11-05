.. index:: single: All Elements In One Equation Set

All Elements In One Equation Set
================================

.. rule::
   :filename: all_elements_in_one_equation_set.py
   :class: AllElementsInOneEquationSet
   :id: id_0003
   :reference: n/a
   :kind: generic
   :tags: modelling

   All elements in equation set

Description
-----------

.. start_description

All elements within a diagram belong to at least one equation set.

.. end_description

Rationale
---------
This enforces compliance with a specific traceability strategy by ensuring that all elements are part of an equation set.

Verification
------------
This rule checks all diagram elements in the model and fails if at least one is not part of an equation set.

Resolution
----------
Add the offending element to an equation set.

Customization
-------------
N/A.
