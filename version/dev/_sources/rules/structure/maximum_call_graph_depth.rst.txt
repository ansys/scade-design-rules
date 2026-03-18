.. index:: single: Maximum call graph depth

Maximum call graph depth
########################

.. rule::
   :filename: maximum_call_graph_depth.py
   :class: MaximumCallGraphDepth
   :id: id_0039
   :reference: n/a
   :kind: generic
   :tags: structure

   Maximum call graph depth

Description
===========

.. start_description

Maximum depth of the call graph shall not exceed 'parameter'.
Check is performed on only public or all operators. Parameter: depth=:maximum value, visibility=Public,ALL (e.g.: depth=7,visibility=Public)

.. end_description

Rationale
=========
This enforces compliance with a specific modeling standard by placing an upper bound on how many operator calls may be nested.

Verification
============
This rule checks all model operators. Depending on parameter ``visibility``, it may skip non-public operators.

For each checked operator, the rule uses a recursive, depth-first algorithm to find the longest chain of nested operator calls.
The rule fails if the resulting longest chain of calls exceeds the authorized ``depth``.

Note: an operator calling no other operators has depth ``1``.

Resolution
==========
Consider refactoring the model to reduce call graph depth, as detailed in the rule failure message.

Customization
=============
N/A.
