.. index:: single: No Terminations

No Terminations
===============

.. rule::
   :filename: no_terminations.py
   :class: NoTerminations
   :id: id_0063
   :reference: n/a
   :kind: generic
   :tags: modelling

   No terminations

Description
-----------

.. start_description

Terminations should not be used.
parameter: 'ALL': all, 'NOIT: do not report terminations at iterator outputs'

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that terminators are not used in models.

Verification
------------
This rule checks all model equations for use of a terminator operator. Depending on rule parameter value, the rule fails for any terminator:

* Anywhere in the model
* Outside of an iterator higher order operator output. Iterator operators are: ``Map``, ``Mapi``, ``Fold``, ``Foldi``, ``MapFold``, ``MapFoldi``.

Resolution
----------
Remove the offending terminator.

Customization
-------------
N/A.
