.. index:: single: Ann notes for named types or variables

Ann notes for named types or variables
######################################

.. rule::
   :filename: ann_notes_for_named_types_or_variables.py
   :class: AnnNotesForNamedTypesOrVariables
   :id: id_0006
   :reference: n/a
   :kind: specific
   :tags: annotations

   AnnotationNotes for variables with basic type

Description
===========

.. start_description

If a variable has a NumericType then the numeric type shall have an annotation with the SI-Units, resolution, etc.
If the variable has a basic type the variable itself shall have the annotation.
If both are defined then raise a warning.
parameter: '-t': Name of the annotation note type: e.g.: '-t SDD_TopLevel'

.. end_description

Rationale
=========
This enforces compliance with a specific modeling standard by ensuring that all named types
or variables don't only show the *what* (the shape of the data itself), but also the *why*,
by documenting what the data corresponds to and what real-world quantities they represent.

Verification
============
This rule checks that all ``NamedType`` or ``Variable`` entities inside the model contain
annotations ``Description`` and ``Constraints``. For all entities that are **not** ``bool``
or ``char`` types, it also checks that they contain annotations ``Min_Value``, ``Max_Value`` and ``Unit_SI``.

Resolution
==========
Modify the offending type or variable to add missing annotations, as detailed in the rule failure message.

Customization
=============
TODO.
