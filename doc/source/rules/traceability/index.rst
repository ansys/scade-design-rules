.. index:: single: Traceability
.. _traceability:

Traceability
============

.. category::
   :name: Traceability

   Set of rules related to the traceability of Scade models.

This section gathers the rules related to the traceability.
Most of them are documented in `ESEG-EN-072 SCADE Traceability`_.
Although each rule can be used separately, it is advised to consider
one of the consistent subsets described in the engineering note,
which are reminded hereafter.

SCADE Suite CE
--------------
cf. `ESEG-EN-072`_, section 3.4

*TRA_REQ_001*: The Contribution Elements are:

* Equation sets
* States
* Transitions
* Textual diagrams

.. topic:: Rules

   .. rules::
      :filter: scade_llr

Only Equation Sets
------------------
cf. `ESEG-EN-072`_, section 3.5.1

*TRA_REQ_001_2*: The Contribution Elements are:

* Equation sets
* Textual diagrams

.. topic:: Rules

   .. rules::
      :filter: only_eqs

Diagrams or Equation Sets
-------------------------
cf. `ESEG-EN-072`_, section 3.5.2

*TRA_REQ_001_3*: The Contribution Elements are:

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

.. _ESEG-EN-072 SCADE Traceability: https://ansys.sharepoint.com/:w:/r/sites/SBUExpertise/Documents/Forms/Engineering%20Notes.aspx?id=%2Fsites%2FSBUExpertise%2FDocuments%2FESEG%2DEN%2D072%20SCADE%20Traceability%2Epdf&parent=%2Fsites%2FSBUExpertise%2FDocuments
.. _ESEG-EN-072: https://ansys.sharepoint.com/:w:/r/sites/SBUExpertise/Documents/Forms/Engineering%20Notes.aspx?id=%2Fsites%2FSBUExpertise%2FDocuments%2FESEG%2DEN%2D072%20SCADE%20Traceability%2Epdf&parent=%2Fsites%2FSBUExpertise%2FDocuments
