.. index:: single: Enumeration has default case

Enumeration has default case
============================

.. rule::
   :filename: enum_has_default_case.py
   :class: EnumHasDefaultCase
   :id: id_0017
   :reference: n/a
   :kind: generic
   :tags: case

   Enum default checked

Description
-----------

.. start_description

In the SCADE model, each enumeration shall use the 'default' for one element to catch any abnormal value.

.. end_description

Rationale
---------
This ensures a defensive design by building abnormal values into every enumeration, promoting correct abnormal value management by all model entities using the enumeration.

Verification
------------
This rule iterates over enumeration definitions and checks that at least one element bears pragma text 'default'.

Resolution
----------
Modify the offending enumeration to add a ``default`` definition, either with one of the "normal" values (such as ``Hold``), or a specifically added value (such as ``Abnormal``).

Customization
-------------
N/A.
