.. index:: single: Default case

Default case
============

.. rule::
   :filename: default_case.py
   :class: DefaultCase
   :id: id_0012
   :reference: SDR-39
   :kind: generic
   :tags: case

   Case default checked

Description
-----------
In the SCADE model, any 'case' construct shall use the 'default' to catch any abnormal value.

Rationale
---------
This ensures a defensive design to catch any abnormal value of enumerated data produced by the environment or by an imported operator.

Verification
------------
The rule registers to the operator calls and raises a violation when all the following conditions are satisfied:

* The called operator is ``case``
* The option ``default`` is not selected

Message: ``Switch without default case.``

Resolution
----------
Add a ``default`` entry to the instance of ``case``, either with one of the "normal" values (such as ``Hold``), or a specifically added value (such as ``Abnormal``).

Customization
-------------
N/A.
