.. index:: single: No Boolean Comparison

No Boolean Comparison
=====================

.. rule::
   :filename: no_bool_comparison.py
   :class: NoBoolComparison
   :id: id_0054
   :reference: n/a
   :kind: generic
   :tags: modelling

   No boolean comparison

Description
-----------

.. start_description

Boolean values should not be compared to the constants TRUE or FALSE

.. end_description

Rationale
---------
This enforces compliance with a specific modeling standard by avoiding redundant expressions involving booleans.

The intent is to improve model conciseness: boolean variables should be used directly instead of being compared with ``TRUE`` or ``FALSE``.

Verification
------------
This rule checks all comparison expressions throughout the model (predefined operators ``=, <>, <, <=, >, >=``).
For each comparison, it recursively determines whether any side of the comparison resolves to a boolean constant, and fails if it finds one.

Resolution
----------
Modify the offending flow to remove the comparison to a constant, and use the boolean value directly.

Customization
-------------
N/A.
