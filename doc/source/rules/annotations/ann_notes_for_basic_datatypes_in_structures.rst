.. index:: single: Ann Notes For Basic Datatypes In Structures

Ann Notes For Basic Datatypes In Structures
===========================================

.. rule::
   :filename: ann_notes_for_basic_datatypes_in_structures.py
   :class: AnnNotesForBasicDataTypesInStructures
   :id: id_0005
   :reference: n/a
   :kind: specific
   :tags: annotations

   AnnotationNotes for basic data types in structures

Description
-----------

.. start_description

Sub-element of structure definitions for component I/O and TPCs that has basic datatypes shall be described with below information in its notes field
- Description:
- Constraints:
If not Booleans
- Min_Value:
- Max_Value:
- Unit(SI):
parameter: '-t': Name of the annotation note type: e.g.: '-t SDD_TopLevel'

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that all structure fields
don't only show the *what* (the shape of the data itself), but also the *why*, by documenting what
the data corresponds to and what real-world quantities they represent.

Verification
------------
This rule checks that all ``NamedType`` entities inside model structures (``CompositeElement``)
contain annotations ``Description`` and ``Constraints``.
For all entities that are **not** ``bool`` or ``char`` types, it also checks that they contain
annotations ``Min_Value``, ``Max_Value`` and ``Unit_SI``.

Resolution
----------
Modify the offending structure element to add missing annotations, as detailed in the rule failure message.

Customization
-------------
TODO.
