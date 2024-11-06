.. index:: single: CE Nature

CE Nature
==========

.. rule::
   :filename: llr_nature.py
   :class: LLRNature
   :id: id_0036
   :reference: TRA_REQ_002
   :tags: scade_llr

   CE must have a design annotation

Description
-----------
The contributing elements shall have an annotation 'DesignElement' with a property 'Nature'.
Parameter: '-t': Name of the note type: e.g.: '-t DesignElement'

.. end_description

The parameter allows defining an alternate note type name, with the following syntax:
``-t <note type name>`` (default value: ``-t DesignElement``).

This rules applies to the following elements:

* Equation set
* Text diagram
* State
* Transition

Rationale
---------
The note type ``DesignElement`` is expected to be designed so that the property ``Nature``
is taken into account when exporting the SCADE CEs through SCADE ALM Gateway.

* The export is easier to specify: all the CEs, regardless their nature.
* The analysis of the traceability matrices is made easier by filtering the matrices with respect to this property.

Verification
------------
The rule registers to the CEs and raises a violation when a CE does not have a note of the specified type.

Message: ``the Contributing Element shall have an annotation <note type name>``

Resolution
----------
Create the note instance.

Notes:

* Make sure the annotation rules are specified correctly with respect to the Scade model elements considered as CEs.
* Use the script ``CreateDefaultNotes.tcl`` to create all the missing note instances, accordingly to the annotation rules of the ``aty`` file.

Customization
-------------
The default value of the rule's parameters ``types`` or ``kinds`` can be overridden provided the targeted model elements can be annotated.

Refer to the documentation of the instantiation of a rule for details.

.. seealso::
   * `ESEG-EN-072 SCADE Traceability`_
   * :ref:`traceability`
   * Instantiation of a rule

.. _`ESEG-EN-072 SCADE Traceability`: https://ansys.sharepoint.com/:w:/r/sites/SBUExpertise/Documents/Forms/Engineering%20Notes.aspx?id=%2Fsites%2FSBUExpertise%2FDocuments%2FESEG%2DEN%2D072%20SCADE%20Traceability%2Epdf&parent=%2Fsites%2FSBUExpertise%2FDocuments
