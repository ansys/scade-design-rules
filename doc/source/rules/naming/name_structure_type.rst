.. index:: single: Name Structure Type

Type name structure
===================

.. rule::
   :filename: name_structure_type.py
   :class: NameStructureType
   :id: id_0053
   :reference: n/a
   :kind: specific
   :tags: naming

   Type Name Structure

Description
-----------

.. start_description

Type shall be in lower letters with capital and start/end with specific characters _t, t\_, Type\_

.. end_description

Rule parameters are given as a comma-separated list. Parameters are:

* ``prefix``: expected type name prefix. Default value is empty (no prefix).
* ``suffix``: expected type name suffix. Default value is ``_t``.

Rationale
---------
This enhances the readability of a model through homogeneous naming.

Verification
------------
The rule registers to named types and raises a violation when:

* The name does not match the expected prefix

  Message: ``Type name does not start with <prefix>``

* The name does not match the expected suffix

  Message: ``Type name does not end with <suffix>``

Resolution
----------
Rename the offending type.

Customization
-------------
N/A.
