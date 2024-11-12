.. index:: single: Tracing Elements

Tracing Elements
================

.. rule::
   :filename: llr_only.py
   :class: LLROnly
   :id: id_0037
   :reference: TRA_REQ_007
   :tags: scade_llr

   Tracing elements must be Contribution Elements

Description
-----------
The model elements tracing requirements shall be Contribution Elements (CE).

.. end_description

* Equation set
* Text diagram
* State
* Transition

Rationale
---------
This ensures the consistency of the traceability matrices: The SCADE ALM Gateway exports only the elements defined as CE.

Verification
------------
The rule registers to the elements that can have traceability links
and raises a violation when an element which is not CE has links to high level requirements.

Message: ``the element is not a CE: it shall not trace the requirement(s) <list of requirements ids>``

Resolution
----------
Delete the traceability links.

Customization
-------------
When the list of elements that are considered as LLR differs from the one listed in the description,
derive a new class from ``LLROnly`` and override the function ``is_llr`` as appropriate.

.. seealso::
   * `ESEG-EN-072 SCADE Traceability`
   * :ref:`traceability`
