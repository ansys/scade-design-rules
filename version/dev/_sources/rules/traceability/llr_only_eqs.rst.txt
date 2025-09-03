.. index:: single: Tracing elements are equation sets

Tracing elements are equation sets
##################################

.. rule::
   :filename: llr_only_eqs.py
   :class: LLROnlyEqs
   :id: id_0096
   :reference: TRA_REQ_007
   :tags: only_eqs

   Tracing elements must be Contributing Elements

Description
===========
The model elements tracing requirements shall be Contributing Elements (CE).

.. end_description

* Equation set
* Text diagram

Rationale
=========
This ensures the consistency of the traceability matrices: The SCADE ALM Gateway exports only the elements defined as CE.

Verification
============
The rule registers to the elements that can have traceability links
and raises a violation when an element which is not CE has links to high level requirements.

Message: ``the element is not a LLR: it shall not trace the requirement(s) <list of requirements ids>``

Resolution
==========
Delete the traceability links.

Customization
=============
This rule is already a customization of the rule :ref:`Tracing Elements <RuleLLROnly>`.

Refer to the documentation of the instantiation of a rule for details.

.. seealso::
   * `ESEG-EN-072 SCADE Traceability`
   * :ref:`traceability`
