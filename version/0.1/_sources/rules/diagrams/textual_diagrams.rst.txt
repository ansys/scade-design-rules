.. index:: single: No textual diagrams

No textual diagrams
###################

.. rule::
   :filename: textual_diagrams.py
   :class: TextualDiagrams
   :id: id_0083
   :reference: n/a
   :kind: generic
   :tags: diagrams

   Textual Diagrams should not be used.

Description
===========

.. start_description

This rule checks if Textual Diagrams are used in the project

.. end_description

Rationale
=========
This enforces compliance with a specific modeling standard by ensuring that
the textual Scade language is not used directly in a model.

Verification
============
This rule checks all operators, states, and actions.
For each one, it verifies that there is no raw textual representation, but only graphical diagrams.

Resolution
==========
Replace the offending operator / state machine element with a graphical diagram.

Customization
=============
TODO
