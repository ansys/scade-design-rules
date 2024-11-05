.. index:: single: Forbidden Real Comparisons

Forbidden Real Comparisons
==========================

.. rule::
   :filename: forbidden_real_comparisons.py
   :class: ForbiddenRealComparisons
   :id: id_0024
   :reference: SDR-38
   :kind: generic
   :tags: modelling

   Forbidden real comparisons

Description
-----------
Comparisons of real values are not allowed: = (20, 21, 22, 23, 24, 25)

.. end_description

The parameter defines the list of comparison operators to consider,
using their code, with the following syntax: ``<code> [, <code>]*``
(default value: ``20, 21, 22, 23, 24, 25``).

The codes are defined in the user documentation:

========    ====
Operator    Code
========    ====
<           20
<=          21
>           22
>=          23
=           24
<>          25
========    ====

Rationale
---------
Real numbers shall not be compared but with appropriate justified tolerance.

Verification
------------
The rule registers to the operator calls, and raises a violation for each call which satisfies all these conditions:

1. The called operator is one of those listed in the rule's parameter
2. One of the operands is float, e.g. ``float32`` or ``float64``.

Message: ``Real comparison in <expression>``

.. note::
   A polymorphic type shall be constrained as ``real`` to be considered as ``float``,
   even if the operator has instantiations with float parameters.

Resolution
----------
Use a comparison operator with tolerance.

Customization
-------------
N/A.
