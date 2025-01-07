.. index:: single: Equation in equation set

Equation in equation set
========================

.. rule::
   :filename: eq_in_eq_set.py
   :class: EqInEqSet
   :id: id_0019
   :reference: TRA_REQ_005
   :tags: scade_llr

   Equation or branch belong to at least one equation set

Description
-----------
An equation or a branch shall belong to at least one equation set except following uses cases:

* The element is text: textual diagram, transition's action, textual state, etc.
* The element is in a state without diagram (Embedded state)

Rationale
---------
This ensures the completeness of the traceability matrices once the Contributing Elements (CE) are exported through SCADE ALM Gateway.
Indeed, the equations or branches are not CE and thus, must belong to an equation set.

The states are CE and the ones without diagram are considered as small enough
to not require their content to be part of an additional equation set.
This is a tradeoff and does not prevent the creation of equation sets within the state when it makes sense.

Verification
------------
The rule registers to the equations and branches, and raises a violation when none of the following condition is satisfied.

* The element is not part of an equation set
* The element's scope is a state without diagram

Message: ``the <kind> <scade path> shall belong to at least one equation set``

where ``<kind>`` is either equation or branch.

Resolution
----------
Add the elements to an equation set.

Customization
-------------
N/A.

.. seealso::
   * `ESEG-EN-072 SCADE Traceability`
   * :ref:`traceability`
