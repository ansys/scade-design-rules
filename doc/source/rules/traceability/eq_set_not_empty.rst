.. index:: single: Equation set not empty

Equation set not empty
======================

.. rule::
   :filename: eq_set_not_empty.py
   :class: EqSetNotEmpty
   :id: id_0021
   :reference: TRA_REQ_006
   :tags: scade_llr only_eqs llr_or_net

   Equation set not empty

Description
-----------
An equation set shall contain at least one element.

Rationale
---------
This helps to identify the equation sets not completed or which have become empty after editing a model.
An empty equation set does not make sense for traceability.

Verification
------------
The rule registers to the equation sets and raises a violation when an equation set does not contain any element.

Message: ``equation set <name> must contain at least one element``

Resolution
----------
Delete the equation set.

Customization
-------------
N/A.

.. seealso::
   * `ESEG-EN-072 SCADE Traceability`
   * :ref:`traceability`
