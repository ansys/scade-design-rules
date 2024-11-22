.. index:: single: Name Structure Enumeration Custom1

Name structure enumeration custom1
==================================

.. rule::
   :filename: name_structure_enumeration_custom1.py
   :class: NameStructureEnumerationCustom1
   :id: id_0109
   :reference: n/a
   :kind: specific
   :tags: naming

   Enumeration Name Structure Custom1

Description
-----------

.. start_description

The Model Designer shall prefix enumeration literal with the enumeration type name (excluding the 'Type' suffix).
parameter: suffix

.. end_description

The rule parameter describes the expected suffix for enumeration type names. Default value is ``Type``.

E.g.: an enumeration value of type ``CoordinateType`` shall have its name prefixed with ``Coordinate``.

Rationale
---------
This enhances the readability of a model through homogeneous naming.

Verification
------------
The rule registers to enumeration values and raises a violation when:

* The type suffix given as a rule parameter has not been excluded from the type name, before using it as a prefix for the enumeration value name

  Message: ``<name> starts with full type name <type_name_with_suffix>``

* The name does not start with the expected type name

  Message: ``<name> does not start with <type_name>``

Resolution
----------
Rename the offending enumeration value.

Customization
-------------
N/A.
