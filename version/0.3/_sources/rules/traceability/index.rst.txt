.. index:: single: Traceability
.. _traceability:

Traceability
############

.. category::
   :name: Traceability

   Set of rules related to the traceability of Scade models.

This section gathers the rules related to traceability.
Most of them are documented in *ESEG-EN-072 SCADE Traceability*.
Although each rule can be used separately, it is advised to consider
one of the consistent subsets described in the engineering note,
which are reminded hereafter.

SCADE Suite Contributing Elements (CE)
======================================
cf. ``ESEG-EN-072``, section 3.4

*TRA_REQ_001*: The Contributing Elements are:

* Equation sets
* States
* Transitions
* Textual diagrams

.. topic:: Rules

   .. rules::
      :filter: scade_llr

Only Equation Sets
==================
cf. ``ESEG-EN-072``, section 3.5.1

*TRA_REQ_001_2*: The Contributing Elements are:

* Equation sets
* Textual diagrams

.. topic:: Rules

   .. rules::
      :filter: only_eqs

Diagrams or Equation Sets
=========================
cf. ``ESEG-EN-072``, section 3.5.2

*TRA_REQ_001_3*: The Contributing Elements are:

* Equation sets
* States
* Transitions
* Textual diagrams
* Diagrams without equation sets

.. topic:: Rules

   .. rules::
      :filter: llr_or_net

.. toctree::
   :titlesonly:
   :hidden:
   :glob:

   *
