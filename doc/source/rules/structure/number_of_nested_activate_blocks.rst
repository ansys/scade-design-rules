.. index:: single: Number Of Nested Activate Blocks

Number Of Nested Activate Blocks
================================

.. rule::
   :filename: number_of_nested_activate_blocks.py
   :class: NumberOfNestedActivateBlocks
   :id: id_0069
   :reference: n/a
   :kind: generic
   :tags: structure

   Number of nested Activate Blocks

Description
-----------

.. start_description

Number of hierarchical levels of conditional blocks ('If Block', 'When Block').
Parameter: maximum value: e.g.: '7'

.. end_description

The rule parameter is an integer value describing the maximum authorized depth for nested conditional blocks. Default value is ``7``.

Rationale
---------
This enforces compliance with a specific modeling standard by placing an upper bound on the depth of nested conditional blocks.

Verification
------------
This rule checks all Activate Blocks (If Blocks or When Blocks) throughout the model.
For each, it uses a recursive depth-first algorithm to determine the maximum number of nested conditional blocks.

The rule traverses nested state machines to look for enclosed conditional blocks.
A conditional block with no nested sub-block has a depth of ``1``.

The rule fails if the maximum number of nested activate blocks exceeds the authorized value.

Resolution
----------
Consider refactoring the offending chain of nested activate blocks to reduce its depth, as detailed in the rule failure message.

Customization
-------------
N/A.
