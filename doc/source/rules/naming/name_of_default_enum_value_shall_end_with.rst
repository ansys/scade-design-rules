.. index:: single: Name Of Default Enum Value Shall End With

Name Of Default Enum Value Shall End With
=========================================

.. rule::
   :filename: name_of_default_enum_value_shall_end_with.py
   :class: NameOfDefaultEnumValueShallEndWith
   :id: id_0120
   :reference: n/a
   :kind: specific
   :tags: naming

   Default Enum Value shall end with

Description
-----------

.. start_description

Name of enum values with the default pragma shall end with 'parameter'
parameter: starting string e.g. 'enumvalue_DEFAULT'

.. end_description

The rule parameter describes the desired suffix. Default value is ``_DEFAULT``.

Rationale
---------
This enhances the readability of a model through homogeneous naming.

Verification
------------
The rule registers to enum values bearing the ``default`` pragma. It raises a violation when the element name does not end with the expected suffix.

  Message: ``Enum value name does not end with <parameter>``

Resolution
----------
Rename the offending enum value.

Customization
-------------
N/A.
