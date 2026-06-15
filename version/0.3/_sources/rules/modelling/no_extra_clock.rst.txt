.. index:: single: No extra clock

No extra clock
##############

.. rule::
   :filename: no_extra_clock.py
   :class: NoExtraClock
   :id: id_0055
   :reference: n/a
   :kind: generic
   :tags: modelling

   No extra clock

Description
===========

.. start_description

Extra clock definitions are not allowed. See When entry in SCADE.

.. end_description

Rationale
=========
This enforces compliance with a specific modeling standard by ensuring that users avoid defining multi-rate applications.

Multi-rate applications, supported by the Merge / When / clock attribute constructs,
allow a SCADE program to compute different parts of its logic at different temporal rates.

Development of multi-rate applications is complex by nature and some projects may want to avoid it altogether.

Verification
============
The rule registers to local variables and raises a violation if one is a When block or a clock.

  Message: ``Extra Clock found``

Resolution
==========
Remove the offending When block or clock.

Customization
=============
N/A.
