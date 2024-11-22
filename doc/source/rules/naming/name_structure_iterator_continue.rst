.. index:: single: Iterator Exit Condition

Iterator exit condition
=======================

.. rule::
   :filename: name_structure_iterator_continue.py
   :class: NameStructureIteratorContinue
   :id: id_0050
   :reference: SDR-20
   :kind: generic
   :tags: naming

   Name structure of iterator exit condition

Description
-----------
For iterators which use an exit condition (mapw, mapwi, foldw, foldwi, mapfoldw, mapfoldwi), the output corresponding to the exit condition should be named 'continue'.

.. end_description

The parameter allows defining an alternate name, with the following syntax: ``-c <regular expression>`` (default value: ``-c continue``).

Rationale
---------
This enhances the readability of a model through homogeneous naming.

Verification
------------
The rule registers to the outputs of operators and raises a violation for each output which satisfies all these conditions:

1. The operator is instantiated with an iterator with exit condition (``mapw``, ``mapwi``, ``foldw``, ``foldwi``, ``mapfoldw``, ``mapfoldwi``)
2. The output corresponds to the exit condition
3. The name of the output does not match the regular expression specified in the rule's parameter

   Message: ``The name does not match the exit condition expression <regexp>``

Resolution
----------
Rename the output.

Customization
-------------
N/A.

.. seealso::
   * :ref:`Name structure of iterator index <RuleNameStructureIteratorIndex>`
   * :ref:`Name structure of accumulator inputs/outputs <RuleNameStructureFoldAccumulator>`
