.. index:: single: Name of default enumeration value shall end with

Name of default enumeration value shall end with
################################################

.. rule::
   :filename: name_of_default_enum_value_shall_end_with.py
   :class: NameOfDefaultEnumValueShallEndWith
   :id: id_0120
   :reference: n/a
   :kind: specific
   :tags: naming

   Default Enum Value shall end with

Description
===========

.. start_description

Name of enumeration values with the default pragma shall end with 'parameter'
parameter: starting string, for example: 'enumvalue_DEFAULT'

.. end_description

The rule parameter describes the desired suffix. Default value is ``_DEFAULT``.

Rationale
=========
This enhances the readability of a model through homogeneous naming.

Verification
============
The rule registers to enumeration values bearing the ``default`` pragma. It raises a violation when the element name does not end with the expected suffix.

  Message: ``Enum value name does not end with <parameter>``

Resolution
==========
Rename the offending enumeration value.

Customization
=============
N/A.
