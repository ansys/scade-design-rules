.. index:: single: No imported operators

No imported operators
#####################

.. rule::
   :filename: no_imported_operators.py
   :class: NoImportedOperators
   :id: id_0042
   :reference: n/a
   :kind: generic
   :tags: operators

   Imported operators shall not be used.

Description
===========

.. start_description

This rule checks if imported operators are used in the project

.. end_description

Rationale
=========
This enforces compliance with a specific modeling standard by ensuring that no external source code is called by model operators.

Verification
============
This rule checks all model operators and fails if it finds one that is imported.

Resolution
==========
Remove the offending operator.

Customization
=============
N/A.
