.. index:: single: Element in Equation Set

Element in Equation Set
=======================

.. rule::
   :filename: all_in_eq_set.py
   :class: AllInEqSet
   :id: id_0093
   :reference: TRA_REQ_005_2
   :tags: only_eqs

   The element belong to at least one equation set

Description
-----------
The elements, except actions, assertions, and control blocks, shall belong to at least one equation set, except following use case:

* The element is text: textual diagram, textual scope

Rationale
---------
This ensures the completeness of the traceability matrices once the Contribution Elements (CE), for example equation sets,
are exported through SCADE ALM Gateway. Indeed, the listed elements are not CE and thus, must belong to an equation set.

Verification
------------
The rule registers to the listed elements (equations, branches, states, and transitions),
and raises a violation when the following conditions are satisfied:

* The element has a graphical representation
* The element does not belong to an equation set.

Message: ``the element <scade path> shall belong to at least one equation set``

Resolution
----------
Add the elements to an equation set.

Customization
-------------
N/A.

.. seealso::
   * `ESEG-EN-072 SCADE Traceability`
   * :ref:`traceability`
