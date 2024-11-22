.. index:: single: CE nature equation set

CE nature equation set
======================

.. rule::
   :filename: llr_nature_eqs.py
   :class: LLRNatureEqs
   :id: id_0095
   :reference: TRA_REQ_002
   :tags: only_eqs

   Contributing elements must have a design annotation

Description
-----------
The Contributing Elements (CE) shall have an annotation 'DesignElement' with a property 'Nature'.
Parameter: '-t': Name of the note type: e.g.: '-t DesignElement'

.. end_description

The parameter allows defining an alternate note type name, with the following syntax:
``-t <note type name>`` (default value: ``-t DesignElement``).

This rules applies to the following elements:

* Equation set
* Text diagram

Rationale
---------
The note type ``DesignElement`` is expected to be designed so that the property ``Nature``
is taken into account when exporting the SCADE Contributing Elements (CE) through SCADE ALM Gateway.

* The export is easier to specify: all the CE, regardless their nature.
* The analysis of the traceability matrices is made easier by filtering the matrices with respect to this property.

Verification
------------
The rule registers to the CE and raises a violation when a CE does not have a note of the specified type.

Message: ``the Low Level Requirement shall have an annotation <note type name>``

Resolution
----------
Create the note instance.

Notes:

* Make sure the annotation rules are specified correctly with respect to the Scade model elements considered as CE.
* Use the script ``CreateDefaultNotes.tcl`` to create all the missing note instances,
  accordingly to the annotation rules of the ``aty`` file.

Customization
-------------
This rule is already a customization of the rule :ref:`CE Nature <RuleLLRNature>`.

Refer to the documentation of the instantiation of a rule for details.

.. seealso::
   * `ESEG-EN-072 SCADE Traceability`
   * :ref:`traceability`
   * Instantiation of a rule
