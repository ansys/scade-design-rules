.. index:: single: All private operators are used

All private operators are used
##############################

.. rule::
   :filename: all_private_operators_are_used.py
   :class: AllPrivateOperatorsAreUsed
   :id: id_0004
   :reference: n/a
   :kind: generic
   :tags: modelling

   All private operators are used

Description
===========

.. start_description

All private operators are called at least once.

.. end_description

Rationale
=========
This enforces compliance with a specific modeling standard by ensuring that all private operators are called at least once.

The intent is to prevent needless review or analysis work on design elements that cannot be traced to requirements.
This rule eases discovery of such items early in the modeling process.

Verification
============
This rule checks that all model operators that have "Private" visibility have at least one expression calling them.

Resolution
==========
Either remove the offending private operator or make it public if appropriate.

Customization
=============
N/A.
