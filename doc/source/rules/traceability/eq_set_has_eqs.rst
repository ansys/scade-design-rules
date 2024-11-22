.. index:: single: Equation Set Content

Equation set content
====================

.. rule::
   :filename: eq_set_has_eqs.py
   :class: EqSetHasEqs
   :id: id_0020
   :reference: TRA_REQ_004
   :tags: scade_llr llr_or_net

   Equation set content

Description
-----------
An equation set shall contain only:

* Equations
* If nodes
* When branches
* Assertions

Rationale
---------
An equation set can contain any element displayed in a graphical diagram.
This rule avoids having Contributing Elements (CE), for example a state or a transition, included in another CE.

Verification
------------
The rule registers to the equation sets and raises a violation when an equation set contains one or more elements not listed.

Message: ``equation set <name> shall not contain <list of elements>``

Resolution
----------
Remove the elements from the equation set.

Customization
-------------
When the list of elements that can be contained by an equation set differs from the one listed in the description,
derive a new class from ``EqSetHasEqs`` and override the function ``accept`` as appropriate.

.. seealso::
   * `ESEG-EN-072 SCADE Traceability`
   * :ref:`traceability`
   * Instantiation of a rule
