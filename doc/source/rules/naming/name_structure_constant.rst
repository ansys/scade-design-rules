.. index:: single: Name Structure Constant

Name structure constant
=======================

.. rule::
   :filename: name_structure_constant.py
   :class: NameStructureConstant
   :id: id_0046
   :reference: n/a
   :kind: specific
   :tags: naming

   Constant Name Structure

Description
-----------

.. start_description

Constant shall be in capitals letters and start/end with specific character _c, c\_, Const\_

.. end_description

The rule parameter describes the desired prefix (if its ends with a ``_`` character) or suffix (if it starts with a ``_`` character). Default value is ``_c``.

Rationale
---------
This enhances the readability of a model through homogeneous naming.

Verification
------------
The rule registers to constants and raises a violation when:

* The name does not match the expected prefix

  Message: ``Constant name does not start with <prefix>``

* The name does not match the expected suffix

  Message: ``Constant name does not end with <suffix>``

* The name is not in capital letters

  Message: ``Constant is not in capital letters``

Resolution
----------
Rename the offending constant.

Customization
-------------
N/A.
