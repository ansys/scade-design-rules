.. index:: single: Name Structure Enumeration

Name Structure Enumeration
==========================

.. rule::
   :filename: name_structure_enumeration.py
   :class: NameStructureEnumeration
   :id: id_0048
   :reference: n/a
   :kind: specific
   :tags: naming

   Enumeration Name Structure

Description
-----------

.. start_description

Enumeration shall be in capital letters and start/end with specific characters. In addition a three letter abbreviation of the corresponding type shall be available. COL_BLACK_e, e_COL_BLACK

.. end_description

The rule parameter describes the desired prefix (if its ends with a ``_`` character) or suffix (if it starts with a ``_`` character). Default value is ``_e``.

Rationale
---------
This enhances the readability of a model through homogeneous naming.

Verification
------------
The rule registers to enumeration constants and raises a violation when:

* The name does not start with the expected prefix

  Message: ``Enumeration name does not start with <parameter>``

* The name does not end with the expected suffix

  Message: ``Enumeration name does not end with <parameter>``

* The name is not in all capital letters

  Message: ``Enumeration is not in capital letters``

* The name does not include a ``_`` character in the fourth position

  Message: ``Enumeration name does not have a three letter abbreviation``

* The name is shorter than three letters

  Message: ``Enumeration name is too short``

Resolution
----------
Rename the offending enumeration constant.

Customization
-------------
N/A.
