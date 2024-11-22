.. index:: single: Architecture CE

Architecture contributing element
=================================

.. rule::
   :filename: llr_architecture.py
   :class: LLRArchitecture
   :id: id_0035
   :reference: TRA_REQ_003, TRA_REQ_003_3
   :tags: scade_llr llr_or_net

   'Architecture' contributing elements

Description
-----------
Architecture contributing elements can be only equation sets or textual diagrams.

.. end_description

The parameter allows defining an alternate note type name, attribute, or value,
with the following syntax: ``-t <note type name> -a <attribute name> -v <value>``
(default value: ``-t DesignElement -a Nature -v Architecture``).

This rules applies to the following elements:

* Equation set
* Text diagram
* State
* Transition

Rationale
---------
The nature ``Architecture`` is not suitable for Contribution Elements such as State or Transition.

Verification
------------
The rule registers to the states and transitions, and raises a violation
when an element has an annotation attribute (default ``-t DesignElement -a Nature``)
with a given value (default ``Architecture``), as specified in the rule's parameter.

Message: ``The <attribute name> of the Contributing Element can't be '<value>'``

Note: The rule does register to the equation sets or textual diagrams since there is no verification do perform.

Resolution
----------
Change the value of the property.

Customization
-------------
The default value of the rule's parameters ``types`` or ``kinds``
can be overridden provided the targeted model elements can be annotated.

Refer to the documentation of the instantiation of a rule for details.

.. seealso::
   * `ESEG-EN-072 SCADE Traceability`
   * :ref:`traceability`
   * Instantiation of a rule
