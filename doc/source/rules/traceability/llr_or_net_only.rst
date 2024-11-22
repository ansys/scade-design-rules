.. index:: single: Tracing Elements Diagram

Tracing elements or diagrams
============================

.. rule::
   :filename: llr_or_net_only.py
   :class: LLROrNetOnly
   :id: id_0098
   :reference: TRA_REQ_007
   :tags: llr_or_net

   Tracing elements must be Contributing Elements

Description
-----------
The model elements tracing requirements shall be Contributing Elements (CE).

.. end_description

* Equation set
* Text diagram
* Graphical diagram without equation set
* State
* Transition

Rationale
---------
This ensures the consistency of the traceability matrices:
The SCADE ALM Gateway exports only the elements defined as CE.

Verification
------------
The rule registers to the elements that can have traceability links
and raises a violation when an element which is not LLR has links to high level requirements.

Message: ``the element is not a CE: it shall not trace the requirement(s) <list of requirements ids>``

Resolution
----------
Delete the traceability links.

Customization
-------------
This rule is already a customization of the rule :ref:`Tracing Elements <RuleLLROnly>`.

Refer to the documentation of the instantiation of a rule for details.

.. seealso::
   * `ESEG-EN-072 SCADE Traceability`
   * :ref:`traceability`
   * Instantiation of a rule
