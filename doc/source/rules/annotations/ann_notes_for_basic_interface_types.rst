.. index:: single: Ann notes for basic interface types

Ann notes for basic interface types
###################################

.. rule::
   :filename: ann_notes_for_basic_interface_types.py
   :class: AnnNotesForBasicInterfaceTypes
   :id: id_0099
   :reference: n/a
   :kind: specific
   :tags: annotations

   AnnotationNotes for basic types in operator interface

Description
===========

.. start_description

All basic types used inside an operator interface shall have an annotation with the SI-Units, resolution, etc.
NamedTypes are checked recursively.
parameter: '-t': Name of the annotation note type, '--public ': Public interfaces only :e.g.: '-t SDD_TopLevel --public'

.. end_description

Rationale
=========
This enforces compliance with a specific modeling standard by ensuring that all
operator interface fields don't only show the *what* (the shape of the data itself),
but also the *why*, by documenting what the data corresponds to
and what real-world quantities they represent.

Verification
============
This rule recursively checks that all types inside operator interfaces contain annotations ``Description`` and ``Constraints``.
For all types that are **not** ``bool`` or ``char``, it also checks that they contain annotations ``Min_Value``, ``Max_Value`` and ``Unit_SI``.

Resolution
==========
Modify the offending operator interface element to add missing annotations, as detailed in the rule failure message.

Customization
=============
TODO.
