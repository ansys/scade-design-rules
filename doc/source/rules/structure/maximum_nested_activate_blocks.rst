.. index:: single: Maximum nested activate blocks

Maximum nested activate blocks
==============================

.. rule::
   :filename: maximum_nested_activate_blocks.py
   :class: MaximumNestedActivateBlocks
   :id: id_0069
   :reference: n/a
   :kind: generic
   :tags: structure

   Maximum nested Activate Blocks

Description
-----------

.. start_description

Maximum hierarchical levels of conditional blocks ('If Block', 'When Block').
Parameter: maximum value: e.g.: '7'

.. end_description

The rule parameter is an integer value describing the maximum authorized depth for nested conditional blocks. Default value is ``7``.

Rationale
---------
This enforces compliance with a specific modeling standard by placing an upper bound on the depth of nested conditional blocks.

Verification
------------
This rule checks all Activate Blocks (If Blocks or When Blocks) throughout the model.
It retrieves the :ref:`Number of nested activate blocks <MetricNumberOfNestedActivateBlocks>` metric associated to each block.

The rule fails if the maximum number of nested activate blocks exceeds the authorized value.

Resolution
----------
Consider refactoring the offending chain of nested activate blocks to reduce its depth, as detailed in the rule failure message.

Customization
-------------
This rule depends on the :ref:`Number of nested activate blocks <MetricNumberOfNestedActivateBlocks>`
metric, that must be included in the package. If you customize the ID of this metric, you must
provide it when instantiating the rule, using the parameter ``metric_id``.

Cf. :ref:`ug_customization` for an example.
