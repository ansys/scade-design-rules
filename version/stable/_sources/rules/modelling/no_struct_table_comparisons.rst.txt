.. index:: single: No struct table comparisons

No struct table comparisons
###########################

.. rule::
   :filename: no_struct_table_comparisons.py
   :class: NoStructTableComparisons
   :id: id_0062
   :reference: n/a
   :kind: generic
   :tags: modelling

   No structure or table comparisons

Description
===========

.. start_description

Structures and/or tables should not be compared directly with each other.

.. end_description

Rationale
=========
This advisory rule helps improve the runtime performance of a model by identifying direct comparisons between structures and/or tables.
These comparison operations go value-by-value and may be costly in terms of compute time.

The intent is to turn this rule on when optimizing for runtime performance in the late stages of model design.

Verification
============
The rule registers to expression calls and raises a violation when a comparison operator [#comp]_ is used between two structures and/or tables [#struct_or_table]_.

.. [#comp] Comparison operators are: ``<``, ``<=``, ``>``, ``>=``, ``=``, ``<>``.

.. [#struct_or_table] Structures or tables are identified either by:

  * A Structure type
  * A Table type
  * Use of any of the following predefined operators: assign a structure element, create a data structure,
    create a data array, convert scalar to vector, Make, Reverse, Transpose, Slice, Concatenation, Map iterators.

Resolution
==========
Modify the offending comparison.

Customization
=============
N/A.
