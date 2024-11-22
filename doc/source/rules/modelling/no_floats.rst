.. index:: single: No Floats

No floats
=========

.. rule::
   :filename: no_floats.py
   :class: NoFloats
   :id: id_0056
   :reference: n/a
   :kind: generic
   :tags: modelling

   No floats

Description
-----------

.. start_description

Floats shall NOT be used

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by forbidding the use of primitive types ``float32`` and ``float64``.

One use case could be to ensure that the model can be run on an embedded target that does not manage floating-point values.

Verification
------------
This rule recursively checks types, variables, constants, and expressions throughout the model for any use of ``float32`` or ``float64``, and fails if any is found.

Resolution
----------
Modify the offending flow to remove the use of ``float32`` or ``float64``.

Customization
-------------
N/A.
