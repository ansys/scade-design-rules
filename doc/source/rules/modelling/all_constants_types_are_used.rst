.. index:: single: All Constants Types Are Used

All Constants Types Are Used
============================

.. rule::
   :filename: all_constants_types_are_used.py
   :class: AllConstantsTypesAreUsed
   :id: id_0002
   :reference: n/a
   :kind: generic
   :tags: modelling

   All constants and types are used at least once

Description
-----------

.. start_description

All constants and types are used at least once.
For constants it is also checked if the annotation note 'only external use' is set.
parameter: '-t': Name of the annotation note type

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by ensuring that each defined constant and type is used at least once in the model.

The intent is to avoid unnecessary definitions. The rule ignores constants marked as externally-used,
as they may not meant to be used directly in the model (for instance, in the case of a library).

Verification
------------
This rule checks all constants and named types. For named types, it checks that there is at least one object using the type.
For constants, it checks that there is either one expression using the constant, or that the constant is annotated as externally used.

Resolution
----------
Remove the unused constant or type.

Customization
-------------
TODO
