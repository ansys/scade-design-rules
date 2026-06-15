.. index:: single: Number of nested activate blocks

Number of nested activate blocks
################################

.. metric::
   :filename: number_of_nested_activate_blocks.py
   :class: NumberOfNestedActivateBlocks
   :id: id_0128
   :reference: n/a
   :kind: specific
   :tags: metrics

   Number of nested activate blocks

Description
===========

.. start_description

Number of nested activate blocks.

.. end_description

Computation
===========
The metric uses a recursive algorithm to determine the maximum number of nested conditional blocks.
It traverses nested state machines to look for enclosed conditional blocks.

A conditional block with no nested sub-block has a depth of ``1``.

Customization
=============
N/A.
