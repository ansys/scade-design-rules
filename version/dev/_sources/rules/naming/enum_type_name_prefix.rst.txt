.. index:: single: Enumeration type name prefix

Enumeration type name prefix
############################

.. rule::
   :filename: enum_type_name_prefix.py
   :class: EnumTypeNamePrefix
   :id: id_0018
   :reference: n/a
   :kind: specific
   :tags: naming

   Enumeration literal prefix check

Description
===========

.. start_description

Checks if the values of a given Enumeration are prefixed with its name

.. end_description

The rule parameter describes a suffix to remove from the enumeration name. Default value is ``Type``.

Rationale
=========
This enforces compliance with a specific modeling standard by ensuring that all names start with the same prefix.

Verification
============
The rule registers to enumeration values. It raises a violation when the name of a value does not start with the expected prefix.

  Message: ``Enumeration literal does not start with <prefix> (Value of <enum_name>)``

The prefix is computed by reading the enumeration name and removing the rule parameter value from its end.

  E.g.: in an enumeration called ``AutopilotModeType``, values are expected to start with ``AutopilotMode``.

Resolution
==========
Rename the offending enumeration value.

Customization
=============
N/A.
